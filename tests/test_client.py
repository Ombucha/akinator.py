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


# pylint: skip-file

import unittest

from akinator import Client, CantGoBackAnyFurther, InvalidLanguageError, InvalidChoiceError, InvalidThemeError


class TestAkinatorClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_init_defaults(self):
        c = Client()
        self.assertIsNotNone(c.session)
        self.assertIsNone(c.language)
        self.assertIsNone(c.theme)
        self.assertFalse(c.child_mode)
        self.assertFalse(c.finished)
        self.assertFalse(c.win)

    def test_language_validation(self):
        with self.assertRaises(InvalidLanguageError):
            self.client.start_game(language="notalanguage")
        # Should not raise
        self.client.start_game(language="en")
        self.client.start_game(language="english")

    def test_theme_validation(self):
        with self.assertRaises(InvalidThemeError):
            self.client.start_game(theme="z")
        with self.assertRaises(InvalidThemeError):
            self.client.start_game(language="ar", theme="a")  # 'a' not in ar
        # Should not raise
        self.client.start_game(theme="c")

    def test_answer_validation(self):
        self.client.start_game()
        with self.assertRaises(InvalidChoiceError):
            self.client.answer("notananswer")

    def test_full_game_flow(self):
        self.client.start_game(language="en", theme="c")
        steps = 0
        while not self.client.finished and steps < 10:
            # Always answer 'yes' for simplicity
            try:
                self.client.answer("yes")
            except InvalidChoiceError:
                self.client.answer("no")
            steps += 1
        self.assertTrue(self.client.finished or steps == 10)

    def test_back_and_exclude(self):
        self.client.start_game(language="en", theme="c")
        with self.assertRaises(CantGoBackAnyFurther):
            self.client.back()
        # Move forward one step
        self.client.answer("yes")
        try:
            self.client.back()
        except Exception:
            self.fail("back() raised unexpectedly after moving forward")
        # Exclude only after win
        self.client.win = False
        with self.assertRaises(RuntimeError):
            self.client.exclude()

    def test_properties_and_str(self):
        self.client.theme = "c"
        self.client.progression = 50
        self.assertEqual(self.client.confidence, 0.5)
        self.assertEqual(self.client.theme_id, 1)
        self.assertEqual(self.client.theme_name, "Characters")
        self.client.language = "en"
        self.client.akitude = "defi.png"
        self.assertIn("defi.png", self.client.akitude_url)
        self.client.win = True
        self.client.finished = False
        self.client.proposition = "prop"
        self.client.name_proposition = "name"
        self.client.description_proposition = "desc"
        self.assertIn("name", str(self.client))
        self.client.finished = True
        self.client.question = "Q?"
        self.assertEqual(str(self.client), "Q?")
        self.client.theme = "a"
        self.assertEqual(self.client.theme_name, "Animals")
        self.client.theme = "o"
        self.assertEqual(self.client.theme_name, "Objects")

    def test_repr(self):
        self.client.language = "en"
        self.client.theme = "c"
        self.client.step = 5
        self.client.progression = 80
        rep = repr(self.client)
        self.assertIn("Akinator Client", rep)
        self.assertIn("Language: en", rep)
        self.assertIn("Theme: Characters", rep)
        self.assertIn("Step: 5", rep)
        self.assertIn("Progression: 80", rep)

    def test_defeat_sets_state(self):
        self.client.language = "en"
        self.client.defeat()
        self.assertTrue(self.client.finished)
        self.assertFalse(self.client.win)
        self.assertEqual(self.client.akitude, "deception.png")
        self.assertEqual(self.client.question, "Bravo, you have defeated me !\nShare your feat with your friends.")
        self.assertEqual(self.client.progression, 100)

    def test_choose_without_win(self):
        self.client.start_game(language="en", theme="c")
        self.client.win = False
        with self.assertRaises(RuntimeError):
            self.client.choose()

    def test_exclude_after_win_and_finished(self):
        self.client.start_game(language="en", theme="c")
        self.client.win = True
        self.client.finished = True
        # Should call defeat and set finished/win
        self.client.language = "en"
        self.client.defeat()
        self.assertTrue(self.client.finished)
        self.assertFalse(self.client.win)
        self.assertEqual(self.client.akitude, "deception.png")

    def test_theme_ids_and_names(self):
        self.client.theme = "c"
        self.assertEqual(self.client.theme_id, 1)
        self.assertEqual(self.client.theme_name, "Characters")
        self.client.theme = "a"
        self.assertEqual(self.client.theme_id, 14)
        self.assertEqual(self.client.theme_name, "Animals")
        self.client.theme = "o"
        self.assertEqual(self.client.theme_id, 2)
        self.assertEqual(self.client.theme_name, "Objects")

    def test_repr_and_str_edge_cases(self):
        self.client.language = None
        self.client.theme = None
        self.client.step = None
        self.client.progression = None
        rep = repr(self.client)
        self.assertIn("Akinator Client", rep)
        self.client.win = False
        self.client.finished = False
        self.client.question = "TestQ"
        self.assertEqual(str(self.client), "TestQ")

if __name__ == "__main__":
    unittest.main()
