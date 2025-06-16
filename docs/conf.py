# pylint: skip-file

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

on_rtd = os.environ.get("READTHEDOCS") == "True"
project = "akinator.py"
copyright = "2025, Omkaar"
author = "Ombucha"
release = "2.0.1"

extensions = ["sphinx.ext.autodoc"]
