sphinxcontrib-markdown
======================
Yet another markdown processor for Sphinx

Setting
=======

Install
-------

::

   $ pip install sphinxcontrib-markdown


Configure Sphinx
----------------

Add ``.md`` to ``source_suffix`` and parser class to ``source_parsers`` in your ``conf.py``::

   source_suffix = ['.rst', '.md']
   source_parsers = {
       '.md': 'sphinxcontrib.markdown.MarkdownParser'
   }
