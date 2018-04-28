# -*- coding: utf-8 -*-

import os
import sys

import pkg_resources
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath('../typepy'))


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {'python': ('http://docs.python.org/', None)}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'typepy'
copyright = u'2017, Tsuyoshi Hombashi'
author = u'Tsuyoshi Hombashi'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = pkg_resources.get_distribution("typepy").version
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pytypeutildoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'typepy.tex', u'typepy Documentation',
     u'Tsuyoshi Hombashi', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'typepy', u'typepy Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'typepy', u'typepy Documentation',
     author, 'typepy', 'One line description of project.',
     'Miscellaneous'),
]


# -- rst_prolog -------------------------------------------
rp_common = u"""
.. |TM| replace:: :superscript:`TM`
"""

rp_builtin = u"""
.. |False| replace:: :py:obj:`False`
.. |True| replace:: :py:obj:`True`
.. |None| replace:: :py:obj:`None`
.. |inf| replace:: :py:obj:`inf`
.. |nan| replace:: :py:obj:`nan`

.. |bool| replace:: :py:class:`bool`
.. |dict| replace:: :py:class:`dict`
.. |int| replace:: :py:class:`int`
.. |list| replace:: :py:class:`list`
.. |float| replace:: :py:class:`float`
.. |str| replace:: :py:class:`str`
.. |tuple| replace:: :py:obj:`tuple`
"""

rp_class = u"""
.. |TypeConversionError| replace:: :py:class:`typepy.TypeConversionError`
.. |DateTime| replace:: :py:class:`typepy.DateTime`
.. |Dictionary| replace:: :py:class:`typepy.Dictionary`
.. |Infinity| replace:: :py:class:`typepy.Infinity`
.. |Integer| replace:: :py:class:`typepy.Integer`
.. |Nan| replace:: :py:class:`typepy.Nan`
.. |NoneType| replace:: :py:class:`typepy.NoneType`
.. |NullString| replace:: :py:class:`typepy.NullString`
.. |RealNumber| replace:: :py:class:`typepy.RealNumber`
.. |String| replace:: :py:class:`typepy.String`
"""

rp_docstring = u"""
.. |result_matrix_desc| replace::
    For each member methods, the result matrix for each ``strict_level`` is as follows.
    Column headers (except ``Method`` column) indicate input data to ``value`` argument of
    a method in the ``Method`` column.
    For each cell shows the output of the method.

.. |strict_level| replace::
    Represents how much strict to detect the value type. Higher strict_level means that more stricter type check.
"""

rst_prolog = (
    rp_common +
    rp_builtin +
    rp_class +
    rp_docstring
)
