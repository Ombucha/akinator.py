# pylint: skip-file

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

on_rtd = os.environ.get("READTHEDOCS") == "True"
project = "akinator.py"
copyright = "2026, Omkaar"
author = "Ombucha"
release = "2.1.0"

extensions = ["sphinx.ext.autodoc"]
