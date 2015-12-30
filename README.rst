sphinxcontrib-markdown
======================
Yet another markdown processor for Sphinx

.. image:: https://travis-ci.org/tk0miya/sphinxcontrib-markdown.svg?branch=master
   :target: https://travis-ci.org/tk0miya/sphinxcontrib-markdown

.. image:: https://coveralls.io/repos/tk0miya/sphinxcontrib-markdown/badge.png?branch=master
   :target: https://coveralls.io/r/tk0miya/sphinxcontrib-markdown?branch=master

.. image:: https://codeclimate.com/github/tk0miya/sphinxcontrib-markdown/badges/gpa.svg
   :target: https://codeclimate.com/github/tk0miya/sphinxcontrib-markdown

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
