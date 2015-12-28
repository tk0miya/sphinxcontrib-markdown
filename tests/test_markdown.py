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
    def test_simple(self):
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

    def test_deep_sections(self):
        markdown = u"""
        # Headings 1
        ## Headings 2
        ### Headings 3
        #### Headings 4
        ##### Headings 5
        ###### Headings 6
        ####### Headings 7
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(7, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings 1', doc[0].astext())
        self.assertIsInstance(doc[1], nodes.section)
        self.assertEqual('Headings 2', doc[1].astext())
        self.assertIsInstance(doc[2], nodes.section)
        self.assertEqual('Headings 3', doc[2].astext())
        self.assertIsInstance(doc[3], nodes.section)
        self.assertEqual('Headings 4', doc[3].astext())
        self.assertIsInstance(doc[4], nodes.section)
        self.assertEqual('Headings 5', doc[4].astext())
        self.assertIsInstance(doc[5], nodes.section)
        self.assertEqual('Headings 6', doc[5].astext())
        self.assertIsInstance(doc[6], nodes.section)
        self.assertEqual('# Headings 7', doc[6].astext())

    def test_bullet_list(self):
        markdown = u"""
        # Headings

        * Item 1
        * Item 2
        * Item 3
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(2, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0].astext())

        self.assertIsInstance(doc[1], nodes.bullet_list)
        self.assertEqual(3, len(doc[1]))
        self.assertIsInstance(doc[1][0], nodes.list_item)
        self.assertEqual(1, len(doc[1][0]))
        self.assertIsInstance(doc[1][0][0], nodes.Text)
        self.assertEqual('Item 1', doc[1][0][0])
        self.assertIsInstance(doc[1][1], nodes.list_item)
        self.assertEqual('Item 2', doc[1][1].astext())
        self.assertIsInstance(doc[1][2], nodes.list_item)
        self.assertEqual('Item 3', doc[1][2].astext())

    def test_ol(self):
        markdown = u"""
        # Headings

        1. Item 1
        2. Item 2
        3. Item 3
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(2, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0].astext())

        self.assertIsInstance(doc[1], nodes.enumerated_list)
        self.assertEqual(3, len(doc[1]))
        self.assertIsInstance(doc[1][0], nodes.list_item)
        self.assertEqual(1, len(doc[1][0]))
        self.assertIsInstance(doc[1][0][0], nodes.Text)
        self.assertEqual('Item 1', doc[1][0][0])
        self.assertIsInstance(doc[1][1], nodes.list_item)
        self.assertEqual('Item 2', doc[1][1].astext())
        self.assertIsInstance(doc[1][2], nodes.list_item)
        self.assertEqual('Item 3', doc[1][2].astext())
