# pylint: skip-file

from pathlib import Path

from setuptools import setup

HERE = Path(__file__).resolve().parent
README = (HERE / "README.rst").read_text()

setup(
    name = "akinator",
    version = "2.0.2",
    description = "A basic API wrapper for Akinator.",
    long_description = README,
    long_description_content_type = "text/x-rst",
    url = "https://github.com/Ombucha/akinator.py",
    author = "Omkaar",
    author_email = "omkaar.nerurkar@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>= 3.9.0',
    packages = ["akinator"],
    include_package_data = True,
    install_requires = ["cloudscraper"]
)
