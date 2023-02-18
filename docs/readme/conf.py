"""Sphinx configuration."""
from pathlib import Path

extensions = [
    'sphinxcontrib.restbuilder',
]

master_doc = Path(__file__).parent.name.upper()
