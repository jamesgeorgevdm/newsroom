# Configuration file for the Sphinx documentation builder.
import sphinx_rtd_theme
# -- Project information -----------------------------------------------------

project = 'newsroom'
copyright = '2025, James van der Merwe'
author = 'James van der Merwe'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx.ext.apidoc',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Django setup ------------------------------------------------------------
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../newsroom'))
sys.path.insert(0, os.path.abspath('../news_room'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'newsroom.settings'
django.setup()

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]