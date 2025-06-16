akinator.py
==========

Installation
------------

**Python 3.8 or higher is required.**

To install the stable version, do the following:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "akinator"

    # Windows
    py -m pip install "akinator"


To install the development version, do the following:

.. code-block:: sh

    $ git clone https://github.com/Ombucha/akinator.py

Make sure you have the latest version of Python installed, or if you prefer, a Python version of 3.8 or greater.

If you have have any other issues feel free to search for duplicates and then create a new issue on GitHub with as much detail as possible. Include the output in your terminal, your OS details and Python version.


Client
-----

.. autoclass:: akinator.Client
    :members:

.. autoclass:: akinator.Akinator
    :members:

.. autoclass:: akinator.AsyncClient
    :members:

.. autoclass:: akinator.AsyncAkinator
    :members:

Exceptions
---------------

.. autoclass:: akinator.AkinatorException
    :members:

.. autoclass:: akinator.CantGoBackAnyFurther
    :members:

.. autoclass:: akinator.InvalidChoiceError
    :members:

.. autoclass:: akinator.InvalidThemeError
    :members:

.. autoclass:: akinator.InvalidLanguageError
    :members:
