#!/usr/bin/env python

from __future__ import absolute_import

import re
from markdown import Markdown
from markdown.util import AMP_SUBSTITUTE
from markdown.odict import OrderedDict
from docutils import nodes

try:
    from html import entities
except ImportError:
    import htmlentitydefs as entities

MAILTO = ('\x02amp\x03#109;\x02amp\x03#97;\x02amp\x03#105;\x02amp\x03#108;'
          '\x02amp\x03#116;\x02amp\x03#111;\x02amp\x03#58;\x02')


class SectionPostprocessor(object):
    def run(self, node):
        i = 0
        while i < len(node):
            if isinstance(node[i], nodes.section):
                for subnode in node[i + 1:]:
                    if isinstance(subnode, nodes.section) and subnode['level'] == node[i]['level']:
                        break
                    node.remove(subnode)
                    node[i] += subnode

                self.run(node[i])

            i += 1

        return node


class StripPostprocessor(object):
    def run(self, node):
        class FakeStripper(object):
            def strip(self):
                return node

        return FakeStripper()


def unescape_char(text):
    unescape = lambda x: chr(int(x.group(1)))
    return re.sub('\x02(\d\d)\x03', unescape, text)


def unescape_email(text):
    result = []
    n = len(AMP_SUBSTITUTE)
    for char in text.split(';'):
        if char.startswith(AMP_SUBSTITUTE + "#"):
            result.append(chr(int(char[n + 1:])))
        elif char.startswith(AMP_SUBSTITUTE):
            result.append(entities.name2codepoint.get(char[n:]))
        else:
            result.append(char)
    return ''.join(result)


class Serializer(object):
    def __call__(self, element):
        return self.visit(element)

    def visit(self, element):
        method = "visit_%s" % element.tag
        if not hasattr(self, method):
            raise RuntimeError('Unknown element: %r' % element)
        else:
            return getattr(self, method)(element)

    def make_node(self, cls, element):
        node = cls()
        if element.text and element.text != "\n":
            node += nodes.Text(unescape_char(element.text))
        for child in element:
            node += self.visit(child)
            if child.tail and child.tail != "\n":
                node += nodes.Text(unescape_char(child.tail))

        return node

    def visit_div(self, element):
        return self.make_node(nodes.container, element)

    def visit_headings(self, element):
        section = nodes.section(level=int(element.tag[1]))
        section += self.make_node(nodes.title, element)
        return section

    visit_h1 = visit_headings
    visit_h2 = visit_headings
    visit_h3 = visit_headings
    visit_h4 = visit_headings
    visit_h5 = visit_headings
    visit_h6 = visit_headings

    def visit_p(self, element):
        return self.make_node(nodes.paragraph, element)

    def visit_em(self, element):
        return self.make_node(nodes.emphasis, element)

    def visit_strong(self, element):
        return self.make_node(nodes.strong, element)

    def visit_code(self, element):
        return nodes.literal(text=unescape_char(element.text))

    def visit_a(self, element):
        refnode = self.make_node(nodes.reference, element)
        href = element.get('href')
        if href:
            if href.startswith(MAILTO):
                refnode['refuri'] = unescape_email(href)
                if href.endswith(refnode[0]):
                    refnode.pop(0)
                    refnode.insert(0, nodes.Text(refnode['refuri'][7:]))  # strip mailto:
            else:
                refnode['refuri'] = href
        if element.get('title'):
            refnode.pop(0)
            refnode.insert(0, nodes.Text(unescape_char(element.get('title'))))
        return refnode

    def visit_img(self, element):
        image = self.make_node(nodes.image, element)
        if element.get('alt'):
            image['alt'] = unescape_char(element.get('alt'))
        if element.get('src'):
            image['uri'] = unescape_char(element.get('src'))
        return image

    def visit_ul(self, element):
        return self.make_node(nodes.bullet_list, element)

    def visit_ol(self, element):
        return self.make_node(nodes.enumerated_list, element)

    def visit_li(self, element):
        return self.make_node(nodes.list_item, element)

    def visit_pre(self, element):
        return nodes.literal_block(text=unescape_char(element[0].text))

    def visit_blockquote(self, element):
        return nodes.literal_block(text=unescape_char(element[0].text))


def md2node(text):
    md = Markdown()
    md.serializer = Serializer()
    md.stripTopLevelTags = False
    md.postprocessors = OrderedDict()
    md.postprocessors['section'] = SectionPostprocessor()
    md.postprocessors['strip'] = StripPostprocessor()
    return md.convert(text)
