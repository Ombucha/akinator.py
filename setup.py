from setuptools import setup
import os

DIRECTORY = os.path.dirname(__file__)

EXTRAS = {
    "async": ["aiohttp"],
    "fast_async": ["aiohttp", "cchardet", "aiodns"]
}
READ_ME = open(os.path.join(DIRECTORY, "README.rst")).read()

setup(
    name = "akinator",
    version = "1.0.2",
    author = "Omkaar",
    author_email = "omkaar.nerurkar@gmail.com",
    packages = ["akinator", "akinator.async_aki"],
    package_data = {
        "akinator": ["VERSION.txt"]
    },
    url = "https://github.com/Infiniticity/akinator.py",
    project_urls = {
        "Documentation": "https://akinator.readthedocs.io",
        "Source": "https://github.com/Infiniticity/akinator.py",
        "Tracker": "https://github.com/Infiniticity/akinator.py/issues",
    },
    license = "MIT License",
    description = "An API wrapper for Akinator.",
    long_description = READ_ME,
    long_description_content_type = "text/x-rst",
    install_requires = ["requests"],
    extras_require = EXTRAS,
    python_requires = ">=3.8.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Topic :: Utilities"
    ]
)
