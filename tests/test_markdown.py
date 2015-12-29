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
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(2, len(doc[0]))
        self.assertIsInstance(doc[0][0], nodes.title)
        self.assertEqual(1, len(doc[0][0]))
        self.assertIsInstance(doc[0][0][0], nodes.Text)
        self.assertEqual('Headings', doc[0][0][0])

        self.assertIsInstance(doc[0][1], nodes.paragraph)
        self.assertEqual(1, len(doc[0][1]))
        self.assertIsInstance(doc[0][1][0], nodes.Text)
        self.assertEqual('Hello world', doc[0][1][0])

    def test_inline(self):
        markdown = u"""
        # Headings with *emphasis* text

        Hello **strong** and `code` world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))
        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(2, len(doc[0]))

        section_title = doc[0][0]
        self.assertIsInstance(section_title, nodes.title)
        self.assertEqual(3, len(section_title))
        self.assertIsInstance(section_title[0], nodes.Text)
        self.assertEqual('Headings with ', section_title[0])
        self.assertIsInstance(section_title[1], nodes.emphasis)
        self.assertEqual('emphasis', section_title[1].astext())
        self.assertIsInstance(section_title[2], nodes.Text)
        self.assertEqual(' text', section_title[2])

        paragraph = doc[0][1]
        self.assertIsInstance(paragraph, nodes.paragraph)
        self.assertEqual(5, len(paragraph))
        self.assertIsInstance(paragraph[0], nodes.Text)
        self.assertEqual('Hello ', paragraph[0])
        self.assertIsInstance(paragraph[1], nodes.strong)
        self.assertEqual('strong', paragraph[1].astext())
        self.assertIsInstance(paragraph[2], nodes.Text)
        self.assertEqual(' and ', paragraph[2])
        self.assertIsInstance(paragraph[3], nodes.literal)
        self.assertEqual('code', paragraph[3].astext())
        self.assertIsInstance(paragraph[4], nodes.Text)
        self.assertEqual(' world', paragraph[4])

    def test_multiple_sections(self):
        markdown = u"""
        # Headings 1

        Hello 1

        ## Headings 1-1

        Hello 1-1

        # Headings 2

        Hello 2

        ## Headings 2-1

        Hello 2-1

        ## Headings 2-2

        Hello 2-2
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(2, len(doc))

        section1 = doc[0]
        self.assertIsInstance(section1, nodes.section)
        self.assertEqual('Headings 1', section1[0].astext())
        self.assertEqual('Hello 1', section1[1].astext())
        self.assertIsInstance(section1[2], nodes.section)
        self.assertEqual('Headings 1-1', section1[2][0].astext())
        self.assertEqual('Hello 1-1', section1[2][1].astext())

        section2 = doc[1]
        self.assertIsInstance(section2, nodes.section)
        self.assertEqual('Headings 2', section2[0].astext())
        self.assertEqual('Hello 2', section2[1].astext())
        self.assertIsInstance(section2[2], nodes.section)
        self.assertEqual('Headings 2-1', section2[2][0].astext())
        self.assertEqual('Hello 2-1', section2[2][1].astext())
        self.assertIsInstance(section2[3], nodes.section)
        self.assertEqual('Headings 2-2', section2[3][0].astext())
        self.assertEqual('Hello 2-2', section2[3][1].astext())

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
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings 1', doc[0][0].astext())
        self.assertIsInstance(doc[0][1], nodes.section)
        self.assertEqual('Headings 2', doc[0][1][0].astext())
        self.assertIsInstance(doc[0][1][1], nodes.section)
        self.assertEqual('Headings 3', doc[0][1][1][0].astext())
        self.assertIsInstance(doc[0][1][1][1], nodes.section)
        self.assertEqual('Headings 4', doc[0][1][1][1][0].astext())
        self.assertIsInstance(doc[0][1][1][1][1], nodes.section)
        self.assertEqual('Headings 5', doc[0][1][1][1][1][0].astext())
        self.assertIsInstance(doc[0][1][1][1][1][1], nodes.section)
        self.assertEqual('Headings 6', doc[0][1][1][1][1][1][0].astext())

        # 7th level headings is recognized as 6th level in markdown-py
        self.assertIsInstance(doc[0][1][1][1][1][2], nodes.section)
        self.assertEqual('# Headings 7', doc[0][1][1][1][1][2][0].astext())

    def test_setext_header(self):
        markdown = u"""
        Headings
        --------

        Hello world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(2, len(doc[0]))
        self.assertIsInstance(doc[0][0], nodes.title)
        self.assertEqual(1, len(doc[0][0]))
        self.assertIsInstance(doc[0][0][0], nodes.Text)
        self.assertEqual('Headings', doc[0][0][0])

        self.assertIsInstance(doc[0][1], nodes.paragraph)
        self.assertEqual(1, len(doc[0][1]))
        self.assertIsInstance(doc[0][1][0], nodes.Text)
        self.assertEqual('Hello world', doc[0][1][0])

    def test_bullet_list(self):
        markdown = u"""
        # Headings

        * Item 1
        * Item 2
        * Item 3
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())

        items = doc[0][1]
        self.assertIsInstance(items, nodes.bullet_list)
        self.assertEqual(3, len(items))
        self.assertIsInstance(items[0], nodes.list_item)
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0], nodes.Text)
        self.assertEqual('Item 1', items[0][0])
        self.assertIsInstance(items[1], nodes.list_item)
        self.assertEqual('Item 2', items[1].astext())
        self.assertIsInstance(items[2], nodes.list_item)
        self.assertEqual('Item 3', items[2].astext())

    def test_nested_bullet_list(self):
        markdown = u"""
        # Headings

        * Item 1
            * Item 1-1
            * Item 1-2
                * Item 1-2-1
        * Item 2
        * Item 3
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())

        items = doc[0][1]
        self.assertIsInstance(items, nodes.bullet_list)
        self.assertEqual(3, len(items))
        self.assertEqual(2, len(items[0]))
        self.assertEqual('Item 1', items[0][0].astext())
        self.assertIsInstance(items[0][1], nodes.bullet_list)
        self.assertEqual('Item 2', items[1].astext())
        self.assertEqual('Item 3', items[2].astext())

        subitems = items[0][1]
        self.assertEqual('Item 1-1', subitems[0].astext())
        self.assertEqual('Item 1-2', subitems[1][0].astext())
        self.assertIsInstance(subitems[1][1], nodes.bullet_list)
        self.assertEqual('Item 1-2-1', subitems[1][1][0].astext())

    def test_ol(self):
        markdown = u"""
        # Headings

        1. Item 1
        2. Item 2
        3. Item 3
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())

        items = doc[0][1]
        self.assertIsInstance(items, nodes.enumerated_list)
        self.assertEqual(3, len(items))
        self.assertIsInstance(items[0], nodes.list_item)
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0], nodes.Text)
        self.assertEqual('Item 1', items[0][0])
        self.assertIsInstance(items[1], nodes.list_item)
        self.assertEqual('Item 2', items[1].astext())
        self.assertIsInstance(items[2], nodes.list_item)
        self.assertEqual('Item 3', items[2].astext())

    def test_codeblock(self):
        markdown = u"""
        # Headings

        He says:

            Hello world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual('He says:', doc[0][1].astext())

        self.assertIsInstance(doc[0][2], nodes.literal_block)
        self.assertEqual('Hello world\n', doc[0][2].astext())

    def test_quote(self):
        markdown = u"""
        # Headings

        He says:

        >Hello world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual('He says:', doc[0][1].astext())

        self.assertIsInstance(doc[0][2], nodes.literal_block)
        self.assertEqual('Hello world', doc[0][2].astext())
