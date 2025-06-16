"""
MIT License

Copyright (c) 2025 Omkaar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class AkinatorException(Exception):
    """Base exception for Akinator-related errors."""

class CantGoBackAnyFurther(AkinatorException):
    """Raised when the user tries to go back but cannot."""
    def __init__(self, message: str = "You are already at the first question."):
        super().__init__(message)

class InvalidLanguageError(AkinatorException):
    """Raised when an invalid language is specified."""
    def __init__(self, message: str = "Invalid language specified."):
        super().__init__(message)

class InvalidChoiceError(AkinatorException):
    """Raised when an invalid choice is made."""
    def __init__(self, message: str = "Invalid choice. Please choose a valid option."):
        super().__init__(message)

class InvalidThemeError(AkinatorException):
    """Raised when an invalid theme is specified."""
    def __init__(self, message: str = "Invalid theme specified."):
        super().__init__(message)
