.. image:: https://raw.githubusercontent.com/Ombucha/akinator.py/main/banner.png

.. image:: https://img.shields.io/pypi/v/akinator
    :target: https://pypi.python.org/pypi/akinator
    :alt: PyPI version
.. image:: https://static.pepy.tech/personalized-badge/akinator?period=total&left_text=downloads&left_color=grey&right_color=red
    :target: https://pypi.python.org/pypi/akinator
    :alt: PyPI downloads
.. image:: https://sloc.xyz/github/Ombucha/akinator.py?lower=True
    :target: https://github.com/Ombucha/akinator.py/graphs/contributors
    :alt: Lines of code
.. image:: https://img.shields.io/github/repo-size/Ombucha/akinator.py?color=yellow
    :target: https://github.com/Ombucha/akinator.py
    :alt: Repository size

A modern, easy-to-use Python wrapper for the Akinator web game, supporting both synchronous and asynchronous usage.

Background
----------

Originally, there was a popular Python library called ``akinator.py``, which provided a simple interface to interact with the Akinator API. However, this library suddenly disappeared from public repositories without notice. In response, a mirror was created here to preserve its functionality. Unfortunately, it too stopped working after Akinator made changes to their backend API. Later, another library called ``akipy`` emerged to fill the gap, but it also became non-functional when Cloudflare protection was introduced on Akinator's endpoints. This library revives Akinator interaction by replacing the standard ``requests`` library with ``cloudscraper``, allowing it to bypass Cloudflare's anti-bot measures and restoring full functionality.

Features
--------

- Play Akinator in Python (sync and async)
- Supports all official Akinator languages and themes
- Simple, Pythonic interface
- Type hints for better editor support
- Custom exceptions for robust error handling
- Well-tested and documented
- Actively maintained and open source

Requirements
------------

- **Python 3.9 or higher**
- `cloudscraper <https://pypi.org/project/cloudscraper/>`_

Installation
------------

To install the latest stable version:

.. code-block:: sh

    python3 -m pip install akinator

To install the development version:

.. code-block:: sh

    git clone https://github.com/Ombucha/akinator.py
    cd akinator.py
    python3 -m pip install -e .

Getting Started
---------------

Synchronous Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import akinator

    aki = akinator.Akinator()
    aki.start_game()

    while not aki.finished:
        print(f"\nQuestion: {str(aki)}")
        user_input = input(
            "Your answer ([y]es/[n]o/[i] don't know/[p]robably/[pn] probably not, [b]ack): "
        ).strip().lower()
        if user_input == "b":
            try:
                aki.back()
            except akinator.CantGoBackAnyFurther:
                print("You can't go back any further!")
        else:
            try:
                aki.answer(user_input)
            except akinator.InvalidChoiceError:
                print("Invalid answer. Please try again.")

    print("\n--- Game Over ---")
    print(f"Proposition: {aki.name_proposition}")
    print(f"Description: {aki.description_proposition}")
    print(f"Pseudo: {aki.pseudo}")
    print(f"Photo: {aki.photo}")
    print(f"Final Message: {aki.question}")


Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    import akinator

    aki = akinator.Akinator()

    async def play():
        await aki.start_game()

        while not aki.finished:
            print(f"\nQuestion: {str(aki)}")
            user_input = input(
                "Your answer ([y]es/[n]o/[i] don't know/[p]robably/[pn] probably not, [b]ack): "
            ).strip().lower()
            if user_input == "b":
                try:
                    await aki.back()
                except akinator.CantGoBackAnyFurther:
                    print("You can't go back any further!")
            else:
                try:
                    await aki.answer(user_input)
                except akinator.InvalidChoiceError:
                    print("Invalid answer. Please try again.")

        print("\n--- Game Over ---")
        print(f"Proposition: {aki.name_proposition}")
        print(f"Description: {aki.description_proposition}")
        print(f"Pseudo: {aki.pseudo}")
        print(f"Photo: {aki.photo}")
        print(f"Final Message: {aki.question}")

    asyncio.run(play())


Advanced Usage
--------------

- **Languages:** All official Akinator languages are supported (see `LANG_MAP` in the code).
- **Themes:** Use "c" for characters, "a" for animals, "o" for objects (not all themes are available in all languages).
- **Error Handling:** All errors raise custom exceptions like `CantGoBackAnyFurther`, `InvalidLanguageError`, `InvalidChoiceError`, and `InvalidThemeError`.
- **Custom Session:** You can pass your own `cloudscraper.CloudScraper` session for advanced usage.
- **Async and Sync:** Both sync and async clients are available for all use cases.
- **Testing:** Comprehensive test suite for both sync and async clients.
- **Examples:** See the `examples/` directory for CLI and bot scripts.

Links
-----

- `Akinator <https://akinator.com/>`_
- `Documentation <https://akinator.readthedocs.io>`_
- `Examples <https://github.com/Ombucha/akinator.py/tree/main/examples>`_
- `PyPI <https://pypi.org/project/akinator.py/>`_

Contributing
------------

Contributions are welcome! Please see the `CONTRIBUTING.md` file for details.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.
