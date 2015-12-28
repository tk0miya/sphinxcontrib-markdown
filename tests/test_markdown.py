# -*- coding: utf-8 -*-

import sys
from docutils import nodes
from textwrap import dedent
from sphinxcontrib.markdown import md2node

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSphinxcontrib(unittest.TestCase):
    def test_simple_markdown(self):
        markdown = u"""
        # Headings

        Hello world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(2, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(1, len(doc[0]))
        self.assertIsInstance(doc[0][0], nodes.title)
        self.assertEqual(1, len(doc[0][0]))
        self.assertIsInstance(doc[0][0][0], nodes.Text)
        self.assertEqual('Headings', doc[0][0][0])

        self.assertIsInstance(doc[1], nodes.paragraph)
        self.assertEqual(1, len(doc[1]))
        self.assertIsInstance(doc[1][0], nodes.Text)
        self.assertEqual('Hello world', doc[1][0])
