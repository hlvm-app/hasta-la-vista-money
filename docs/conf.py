# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import django
import os
import sys


sys.path.insert(0, os.path.abspath('..'))

os.environ.get('DJANGO_SETTINGS_MODULE', 'hasta_la_vista_money.settings')

django.setup()

# Configure the Sphinx Django extension
django_settings = 'hasta_la_vista_money.settings'


project = 'Hasta La Vista Money'
copyright = '2023, Alexander Pavlov'
author = 'Alexander Pavlov'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
