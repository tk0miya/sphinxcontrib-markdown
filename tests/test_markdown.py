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

        * backticks: `e=f()` or ``e=f("`")``
        * escapes: \*hello world*
        * strong-em: ***strongem*** or ***em*strong**
        * em-strong: ***strong**em*
        * smart em: _smart_emphasis_
        * yet another em: _emphasis_
        * stand-alone * or _ (not inline markups)
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))
        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(3, len(doc[0]))

        # Headings with *emphasis* text
        section_title = doc[0][0]
        self.assertIsInstance(section_title, nodes.title)
        self.assertEqual(3, len(section_title))
        self.assertIsInstance(section_title[0], nodes.Text)
        self.assertEqual('Headings with ', section_title[0])
        self.assertIsInstance(section_title[1], nodes.emphasis)
        self.assertEqual('emphasis', section_title[1].astext())
        self.assertIsInstance(section_title[2], nodes.Text)
        self.assertEqual(' text', section_title[2])

        # Hello **strong** and `code` world
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

        items = doc[0][2]
        self.assertIsInstance(items, nodes.bullet_list)
        self.assertEqual(7, len(items))

        # backticks: `e=f()` or ``e=f("`")``
        backticks = items[0][0]
        self.assertIsInstance(backticks, nodes.paragraph)
        self.assertEqual(4, len(backticks))
        self.assertEqual('backticks: ', backticks[0])
        self.assertIsInstance(backticks[1], nodes.literal)
        self.assertEqual('e=f()', backticks[1][0])
        self.assertIsInstance(backticks[2], nodes.Text)
        self.assertEqual(' or ', backticks[2])
        self.assertIsInstance(backticks[3], nodes.literal)
        self.assertEqual('e=f("`")', backticks[3][0])

        # escapes: \*hello world*
        escapes = items[1][0]
        self.assertIsInstance(escapes, nodes.paragraph)
        self.assertEqual(1, len(escapes))
        self.assertIsInstance(escapes[0], nodes.Text)
        self.assertEqual('escapes: *hello world*', escapes[0])

        # strong-em: ***strongem*** or ***em*strong**
        strongem = items[2][0]
        self.assertIsInstance(strongem, nodes.paragraph)
        self.assertEqual(4, len(strongem))
        self.assertIsInstance(strongem[0], nodes.Text)
        self.assertEqual('strong-em: ', strongem[0])
        self.assertIsInstance(strongem[1], nodes.strong)
        self.assertIsInstance(strongem[1][0], nodes.emphasis)
        self.assertEqual('strongem', strongem[1][0][0])
        self.assertIsInstance(strongem[2], nodes.Text)
        self.assertEqual(' or ', strongem[2])
        self.assertIsInstance(strongem[3], nodes.strong)
        self.assertIsInstance(strongem[3][0], nodes.emphasis)
        self.assertEqual('em', strongem[3][0][0])
        self.assertIsInstance(strongem[3][1], nodes.Text)
        self.assertEqual('strong', strongem[3][1])

        # em-strong: ***strong**em*
        emstrong = items[3][0]
        self.assertIsInstance(emstrong, nodes.paragraph)
        self.assertEqual(2, len(emstrong))
        self.assertIsInstance(emstrong[0], nodes.Text)
        self.assertEqual('em-strong: ', emstrong[0])
        self.assertIsInstance(emstrong[1], nodes.emphasis)
        self.assertIsInstance(emstrong[1][0], nodes.strong)
        self.assertEqual('strong', emstrong[1][0][0])
        self.assertIsInstance(emstrong[1][1], nodes.Text)
        self.assertEqual('em', emstrong[1][1])

        # smart em: _smart_emphasis_
        smartem = items[4][0]
        self.assertIsInstance(smartem, nodes.paragraph)
        self.assertEqual(2, len(smartem))
        self.assertIsInstance(smartem[0], nodes.Text)
        self.assertEqual('smart em: ', smartem[0])
        self.assertIsInstance(smartem[1], nodes.emphasis)
        self.assertEqual('smart_emphasis', smartem[1][0])

        # yet another em: _emphasis_
        another_em = items[5][0]
        self.assertIsInstance(another_em, nodes.paragraph)
        self.assertEqual(2, len(another_em))
        self.assertIsInstance(another_em[0], nodes.Text)
        self.assertEqual('yet another em: ', another_em[0])
        self.assertIsInstance(another_em[1], nodes.emphasis)
        self.assertEqual('emphasis', another_em[1][0])

        # stand-alone * or _ (not inline markups)
        standalone = items[6][0]
        self.assertIsInstance(standalone, nodes.paragraph)
        self.assertEqual(1, len(standalone))
        self.assertIsInstance(standalone[0], nodes.Text)
        self.assertEqual('stand-alone * or _ (not inline markups)', standalone[0])

    def test_links(self):
        markdown = u"""
        # Headings

        [Sphinx]: http://sphinx-doc.org/
        [2]: /path/to/image.png
        [3]: http://www.google.com/

        * links:
            * [text](url_1)
            * [text](<url_2>)
            * [Google](url_3 "title")
        * images:
            * ![alttxt](http://x.com/)
            * ![alttxt](<http://x.com/>)
        * references:
            * [Google][3]
            * [Sphinx]
        * image reference: ![alt text][2]
        * autolink:
            * <http://www.123.com>
            * <me@example.com>
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))
        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(2, len(doc[0]))
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual(5, len(doc[0][1]))

        # links:
        #   * [text](url_1)
        #   * [text](<url_2>)
        #   * [Google](url_3 "title")
        links = doc[0][1][0]
        self.assertEqual('links:', links[0].astext())
        items = links[1]
        self.assertEqual(3, len(items))
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0][0], nodes.reference)
        self.assertEqual('url_1', items[0][0][0].get('refuri'))
        self.assertEqual(1, len(items[0][0][0]))
        self.assertEqual('text', items[0][0][0].astext())
        self.assertEqual(1, len(items[1][0]))
        self.assertIsInstance(items[1][0][0], nodes.reference)
        self.assertEqual('url_2', items[1][0][0].get('refuri'))
        self.assertEqual(1, len(items[1][0][0]))
        self.assertEqual('text', items[1][0][0].astext())
        self.assertEqual(1, len(items[2][0]))
        self.assertIsInstance(items[2][0][0], nodes.reference)
        self.assertEqual('url_3', items[2][0][0].get('refuri'))
        self.assertEqual(1, len(items[2][0][0]))
        self.assertEqual('title', items[2][0][0].astext())

        # images:
        #   * ![alttxt](http://x.com/)
        #   * ![alttxt](<http://x.com/>)
        images = doc[0][1][1]
        self.assertEqual('images:', images[0].astext())
        items = images[1]
        self.assertEqual(2, len(items))
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0][0], nodes.image)
        self.assertEqual('http://x.com/', items[0][0][0].get('uri'))
        self.assertEqual('alttxt', items[0][0][0].get('alt'))
        self.assertEqual(0, len(items[0][0][0]))
        self.assertEqual(1, len(items[1][0]))
        self.assertIsInstance(items[1][0][0], nodes.image)
        self.assertEqual('http://x.com/', items[1][0][0].get('uri'))
        self.assertEqual('alttxt', items[1][0][0].get('alt'))
        self.assertEqual(0, len(items[1][0][0]))

        # references:
        #   * [Google][3]
        #   * [Sphinx]
        links = doc[0][1][2]
        self.assertEqual('references:', links[0].astext())
        items = links[1]
        self.assertEqual(2, len(items))
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0][0], nodes.reference)
        self.assertEqual('http://www.google.com/', items[0][0][0].get('refuri'))
        self.assertEqual(1, len(items[0][0][0]))
        self.assertEqual('Google', items[0][0][0].astext())
        self.assertEqual(1, len(items[1][0]))
        self.assertIsInstance(items[1][0][0], nodes.reference)
        self.assertEqual('http://sphinx-doc.org/', items[1][0][0].get('refuri'))
        self.assertEqual(1, len(items[1][0][0]))
        self.assertEqual('Sphinx', items[1][0][0].astext())

        # image reference: ![alt text][2]
        imageref = doc[0][1][3][0]
        self.assertEqual(2, len(imageref))
        self.assertEqual('image reference: ', imageref[0].astext())
        self.assertIsInstance(imageref[1], nodes.image)
        self.assertEqual('/path/to/image.png', imageref[1].get('uri'))
        self.assertEqual('alt text', imageref[1].get('alt'))

        # autolink:
        #   * <http://www.123.com>
        #   * <me@example.com>
        links = doc[0][1][4]
        self.assertEqual('autolink:', links[0].astext())
        items = links[1]
        self.assertEqual(2, len(items))
        self.assertEqual(1, len(items[0]))
        self.assertIsInstance(items[0][0][0], nodes.reference)
        self.assertEqual('http://www.123.com', items[0][0][0].get('refuri'))
        self.assertEqual(1, len(items[0][0][0]))
        self.assertEqual('http://www.123.com', items[0][0][0].astext())
        self.assertEqual(1, len(items[1][0]))
        self.assertIsInstance(items[1][0][0], nodes.reference)
        self.assertEqual('mailto:me@example.com', items[1][0][0].get('refuri'))
        self.assertEqual(1, len(items[1][0][0]))
        self.assertEqual('me@example.com', items[1][0][0].astext())

    def test_html(self):
        markdown = u"""
        # Headings

        * HTML Entities:
            * &amp;
            * &quot;
            * &lt;
            * &gt;
            * &nbsp;
            * &#9999;
        * inline HTML:
            * <span>hello world</span>
            * hello <em>Sphinx</em> world
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))
        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual(2, len(doc[0]))
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual(2, len(doc[0][1]))

        # HTML Entities:
        #   * &amp;
        #   * &quot;
        #   * &lt;
        #   * &gt;
        #   * &nbsp;
        #   * &#9999;
        entities = doc[0][1][0]
        self.assertEqual('HTML Entities:', entities[0].astext())
        items = entities[1]
        self.assertEqual(6, len(items))
        self.assertEqual('&amp;', items[0].astext())
        self.assertEqual('&quot;', items[1].astext())
        self.assertEqual('&lt;', items[2].astext())
        self.assertEqual('&gt;', items[3].astext())
        self.assertEqual('&nbsp;', items[4].astext())
        self.assertEqual('&#9999;', items[5].astext())

        # inline HTML:
        #   * <span>hello world</span>
        #   * hello <em>Sphinx</em> world
        inline_html = doc[0][1][1]
        self.assertEqual('inline HTML:', inline_html[0].astext())
        items = inline_html[1]
        self.assertEqual(2, len(items))
        self.assertIsInstance(items[0][0], nodes.raw)
        self.assertEqual('html', items[0][0]['format'])
        self.assertEqual('<span>hello world</span>', items[0][0][0])
        self.assertIsInstance(items[1][0], nodes.raw)
        self.assertEqual('html', items[1][0]['format'])
        self.assertEqual('hello <em>Sphinx</em> world', items[1][0][0])

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
        self.assertIsInstance(items[0][0], nodes.paragraph)
        self.assertEqual(1, len(items[0][0]))
        self.assertIsInstance(items[0][0][0], nodes.Text)
        self.assertEqual('Item 1', items[0][0][0])
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
        self.assertIsInstance(items[0][0], nodes.paragraph)
        self.assertEqual(1, len(items[0][0]))
        self.assertIsInstance(items[0][0][0], nodes.Text)
        self.assertEqual('Item 1', items[0][0][0])
        self.assertIsInstance(items[1], nodes.list_item)
        self.assertEqual('Item 2', items[1].astext())
        self.assertIsInstance(items[2], nodes.list_item)
        self.assertEqual('Item 3', items[2].astext())

    def test_codeblock(self):
        markdown = u"""
        # Headings

        He says:

            Hello "this *beautiful* world"
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual('He says:', doc[0][1].astext())

        self.assertIsInstance(doc[0][2], nodes.literal_block)
        self.assertEqual('Hello "this *beautiful* world"\n', doc[0][2].astext())

    def test_quote(self):
        markdown = u"""
        # Headings

        He wrote:

        >Hello world
        >
        >She wrote:
        >
        >>Hello "this *beautiful* world"
        """
        doc = md2node(dedent(markdown))
        self.assertIsInstance(doc, nodes.container)
        self.assertEqual(1, len(doc))

        self.assertIsInstance(doc[0], nodes.section)
        self.assertEqual('Headings', doc[0][0].astext())
        self.assertEqual('He wrote:', doc[0][1].astext())

        quote = doc[0][2]
        self.assertIsInstance(quote, nodes.literal_block)
        self.assertIsInstance(quote[0], nodes.paragraph)
        self.assertEqual('Hello world', quote[0].astext())
        self.assertIsInstance(quote[1], nodes.paragraph)
        self.assertEqual('She wrote:', quote[1].astext())
        self.assertIsInstance(quote[2], nodes.literal_block)
        self.assertIsInstance(quote[2][0], nodes.paragraph)
        self.assertIsInstance(quote[2][0][0], nodes.Text)
        self.assertEqual('Hello "this ', quote[2][0][0])
        self.assertIsInstance(quote[2][0][1], nodes.emphasis)
        self.assertEqual('beautiful', quote[2][0][1][0])
        self.assertIsInstance(quote[2][0][2], nodes.Text)
        self.assertEqual(' world"', quote[2][0][2])
