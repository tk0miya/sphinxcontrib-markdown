#!/usr/bin/env python

from __future__ import absolute_import

from markdown import Markdown
from markdown.odict import OrderedDict
from docutils import nodes


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


class Serializer(object):
    def __call__(self, element):
        return self.visit(element)

    def visit(self, element):
        method = "visit_%s" % element.tag
        if not hasattr(self, method):
            raise RuntimeError('Unknown element: %r' % element)
        else:
            return getattr(self, method)(element)

    def visit_div(self, element):
        div = nodes.container()
        for child in element:
            div += self.visit(child)
        return div

    def visit_headings(self, element):
        section = nodes.section(level=int(element.tag[1]))
        section += nodes.title(text=element.text)
        return section

    visit_h1 = visit_headings
    visit_h2 = visit_headings
    visit_h3 = visit_headings
    visit_h4 = visit_headings
    visit_h5 = visit_headings
    visit_h6 = visit_headings

    def visit_p(self, element):
        return nodes.paragraph(text=element.text)

    def visit_ul(self, element):
        ul = nodes.bullet_list()
        for child in element:
            ul += self.visit(child)
        return ul

    def visit_ol(self, element):
        ol = nodes.enumerated_list()
        for child in element:
            ol += self.visit(child)
        return ol

    def visit_li(self, element):
        li = nodes.list_item()
        li += nodes.Text(element.text)
        for child in element:
            li += self.visit(child)
        return li

    def visit_pre(self, element):
        return nodes.literal_block(text=element[0].text)

    def visit_blockquote(self, element):
        return nodes.literal_block(text=element[0].text)


def md2node(text):
    md = Markdown()
    md.serializer = Serializer()
    md.stripTopLevelTags = False
    md.postprocessors = OrderedDict()
    md.postprocessors['section'] = SectionPostprocessor()
    md.postprocessors['strip'] = StripPostprocessor()
    return md.convert(text)
