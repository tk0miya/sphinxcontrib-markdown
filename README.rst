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

Add ``sphinxcontrib.markdown`` to ``extensions`` at `conf.py`::

   extensions += ['sphinxcontrib.markdown']
   source_suffix = ['.rst', '.md']
   source_parsers = {
       '.md': 'sphinxcontrib.markdown.MarkdownParser'
   }
