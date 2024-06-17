# conf.py

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "chiaro"
copyright = "2024, Joseph M Courtney"
author = "Joseph M Courtney"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"
