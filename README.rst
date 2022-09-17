===========
akinator.py
===========

.. image:: https://img.shields.io/github/license/Infiniticity/akinator.py
    :target: https://github.com/Infiniticity/akinator.py/blob/main/LICENSE.md
    :alt: license
.. image:: https://img.shields.io/tokei/lines/github/Infiniticity/akinator.py
    :target: https://github.com/Infiniticity/akinator.py/graphs/contributors
    :alt: lines of code
.. image:: https://img.shields.io/pypi/v/akinator
    :target: https://pypi.python.org/pypi/akinator
    :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/akinator
    :alt: Python version info


**********
Installing
**********

To install the regular library without asynchronous support, just run the following command:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "akinator"

    # Windows
    py -m pip install "akinator"


Otherwise, to get asynchronous support, do:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "akinator[async]"

    # Windows
    py -m pip install "akinator[async]"


To get async support plus faster performance (via the ``aiodns`` and ``cchardet`` libraries), do:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "akinator[fast_async]"

    # Windows
    py -m pip install "akinator[fast_async]"


To install the development version, do the following:

.. code-block:: sh

    git clone https://github.com/Infiniticity/akinator.py


Requirements
============

* Python ≥ 3.8.0

* `requests <https://pypi.python.org/pypi/requests>`_

* `aiohttp <https://pypi.python.org/pypi/aiohttp>`_ (Optional, for async)

* `aiodns <https://pypi.python.org/pypi/aiodns>`_ and `cchardet <https://pypi.python.org/pypi/cchardet>`_ (Optional, for faster performance with async)


Usually ``pip`` will handle these for you.


Links
=====

- `Akinator <https://akinator.com/>`_
- `Documentation <https://akinator.readthedocs.io/>`_
