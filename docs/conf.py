# conf.py

import os
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------

# Add the root directory of the project to sys.path
sys.path.insert(0, str(Path(__file__).parents[2]))

# -- Project information -----------------------------------------------------

project = 'Copcon'
author = 'Kasper Junge'
release = '0.3.2'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',                  # Core autodoc extension
    'sphinx.ext.napoleon',                 # Supports Google-style docstrings
    'sphinx_autodoc_typehints',            # Integrates type hints
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'            # Use the Read the Docs theme
html_static_path = ['_static']
