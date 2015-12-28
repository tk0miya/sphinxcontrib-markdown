#!/usr/bin/env python

from __future__ import absolute_import

from markdown import Markdown
from docutils import nodes


class OutputWrapper(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def strip(self):
        return self.nodes


class Serializer(object):
    def __call__(self, element):
        if isinstance(element, list):
            ret = [self.visit(child) for child in element]
        else:
            ret = self.visit(element)

        return OutputWrapper(ret)

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
        section = nodes.section()
        section += nodes.title(text=element.text, level=int(element.tag[1]))
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
        return li


def md2node(text):
    md = Markdown()
    md.serializer = Serializer()
    md.stripTopLevelTags = False
    md.postprocessors = {}
    return md.convert(text)
