# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# ? insert the project root to let sphinx recognize/find packages
sys.path.insert(0, os.path.abspath(".."))

# ? also import the module itself, to populate static contents like version
sys.path.append(os.path.abspath(".."))
import nlpurify
import nlpurify.legacy # explictly import gh#8

project = 'NLPurify'
copyright = '2024, shark-utilities developers'
author = 'shark-utilities developers'
release = nlpurify.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Autodoc configurations --------------------------------------------------
# https://stackoverflow.com/a/44638788/6623589 reduces code writing at automodule config
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "private-members": True
}

# -- Options for Autodoc Pydantic -------------------------------------------
# https://autodoc-pydantic.readthedocs.io/en/stable/users/installation.html
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
