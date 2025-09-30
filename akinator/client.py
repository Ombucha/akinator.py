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

from typing import Literal, Optional
from re import search
from html import unescape
from cloudscraper import CloudScraper, create_scraper

from .exceptions import CantGoBackAnyFurther, InvalidLanguageError, InvalidChoiceError, InvalidThemeError

LANG_MAP = {
    "english": "en",
    "arabic": "ar",
    "chinese": "cn",
    "german": "de",
    "spanish": "es",
    "french": "fr",
    "hebrew": "il",
    "italian": "it",
    "japanese": "jp",
    "korean": "kr",
    "dutch": "nl",
    "polish": "pl",
    "portuguese": "pt",
    "russian": "ru",
    "turkish": "tr",
    "indonesian": "id",
}

THEME_IDS = {"c": 1, "a": 14, "o": 2}

# c - characters
# a - animals
# o - objects

THEME_MAP = {
    "en": ["c", "a", "o"],
    "ar": ["c"],
    "cn": ["c"],
    "de": ["c", "a"],
    "es": ["c", "a"],
    "fr": ["c", "a", "o"],
    "il": ["c"],
    "it": ["c", "a"],
    "jp": ["c", "a"],
    "kr": ["c"],
    "nl": ["c"],
    "pl": ["c"],
    "pt": ["c"],
    "ru": ["c"],
    "tr": ["c"],
    "id": ["c"],
}

ANSWER_IDS = {
    0: ["yes", "y", "0"],
    1: ["no", "n", "1"],
    2: ["i", "idk", "i dont know", "i don't know", "2"],
    3: ["p", "probably", "3"],
    4: ["pn", "probably not", "4"],
}

ANSWER_MAP = {item: key for key, values in ANSWER_IDS.items() for item in values}

class Client:

    """
    A class representing a client for the Akinator game.

    :param session: An optional `CloudScraper` object to use for making HTTP requests. If not provided, a new session will be created.
    :type session: Optional[CloudScraper]

    :ivar flag_photo: The URL of the flag photo associated with the current game session.
    :ivar photo: The URL of the character photo associated with the current game session.
    :ivar pseudo: The pseudo name of the player in the current game session.
    :ivar theme: The theme of the game session, which can be "c" (characters), "a" (animals), or "o" (objects).
    :ivar session_id: The unique identifier for the current game session.
    :ivar signature: The signature for the current game session.
    :ivar identifiant: The unique identifier for the player in the current game session.
    :ivar child_mode: A boolean indicating whether child mode is enabled for the game session.
    :ivar language: The language used for the game session, represented as a string (e.g., "en" for English).
    :ivar question: The current question being asked in the game session.
    :ivar progression: The progression percentage of the game session, represented as a float.
    :ivar step: The current step number in the game session.
    :ivar akitude: The current akitude image associated with the game session.
    :ivar step_last_proposition: The last proposition made in the current step.
    :ivar finished: A boolean indicating whether the game session has finished.
    :ivar win: A boolean indicating whether the player has won the game session.
    :ivar id_proposition: The unique identifier for the current proposition in the game session.
    :ivar name_proposition: The name of the current proposition in the game session.
    :ivar description_proposition: The description of the current proposition in the game session.
    :ivar proposition: The current proposition being made in the game session.
    :ivar completion: The completion status of the game session, which can be "OK, "KO - TIMEOUT", "SOUNDLIKE", or other values.
    :ivar confidence: The confidence level of the current question, represented as a float between 0 and 1.
    :ivar theme_id: The ID of the current theme, represented as an integer.
    :ivar theme_name: The name of the current theme, represented as a string.
    :ivar akitude_url: The URL of the current akitude image associated with the game session.
    """

    def __init__(self, session: Optional[CloudScraper] = None):
        self.session = session if session else create_scraper()

        self.flag_photo = None
        self.photo = None
        self.pseudo = None
        self.theme = None
        self.session_id = None
        self.signature = None
        self.identifiant = None
        self.child_mode = False
        self.language = None
        self.theme = None

        self.question = None
        self.progression = None
        self.step = None
        self.akitude = None
        self.step_last_proposition = ""
        self.finished = False

        self.win = False
        self.id_proposition = None
        self.name_proposition = None
        self.description_proposition = None
        self.proposition = ""
        self.completion = None

    def __handler(self, response):
        response.raise_for_status()
        try:
            data = response.json()
        except Exception as e:
            if "A technical problem has ocurred." in response.text:
                raise RuntimeError("A technical problem has occurred. Please try again later.") from e
            raise RuntimeError("Failed to parse the response as JSON.") from e

        if "completion" not in data:
            data["completion"] = self.completion
        if data["completion"] == "KO - TIMEOUT":
            raise RuntimeError("The session has timed out. Please start a new game.")
        if data["completion"] == "SOUNDLIKE":
            self.finished = True
            self.win = True
            if not self.id_proposition:
                self.defeat()
        elif "id_proposition" in data:
            self.win = True
            self.id_proposition = data["id_proposition"]
            self.name_proposition = data["name_proposition"]
            self.description_proposition = data["description_proposition"]
            self.step_last_proposition = self.step
            self.pseudo = data["pseudo"]
            self.flag_photo = data["flag_photo"]
            self.photo = data["photo"]
        else:
            self.akitude = data["akitude"]
            self.step = int(data["step"])
            self.progression = float(data["progression"])
            self.question = data["question"]
        self.completion = data["completion"]

    def start_game(self, *, language: str = "en", child_mode: bool = False, theme: Literal["c", "a", "o"] = "c"):
        """
        Starts a new game session with the specified language, child mode, and theme.

        :param language: The language to use for the game. Defaults to "en" (English).
        :type language: str
        :param child_mode: Whether to enable child mode. Defaults to False.
        :type child_mode: bool
        :param theme: The theme to use for the game. Can be "c" (characters), "a" (animals), or "o" (objects). Defaults to "c".
        :type theme: Literal["c", "a", "o"]
        """
        if language not in LANG_MAP and language not in LANG_MAP.values():
            raise InvalidLanguageError(f"Unsupported language: {language}. Supported languages: {', '.join(LANG_MAP.keys())}")

        if theme not in THEME_IDS and theme not in THEME_IDS.values():
            raise InvalidThemeError(f"Unsupported theme: {theme}. Supported themes: {', '.join(THEME_IDS.keys())}")

        if theme not in THEME_MAP[LANG_MAP.get(language.lower(), language.lower())]:
            raise InvalidThemeError(f"Theme '{theme}' is not available for language '{language}'.")

        try:
            self.theme = theme
            self.language = LANG_MAP.get(language.lower(), language.lower())
            self.child_mode = child_mode

            response = self.session.post(f"https://{self.language}.akinator.com/game", data={"sid": THEME_IDS[theme], "cm": str(child_mode).lower()})
            response.raise_for_status()
            text = response.text

            self.session_id = search(r"#session'\).val\('(.+?)'\)", text).group(1)
            self.signature = search(r"#signature'\).val\('(.+?)'\)", text).group(1)
            self.identifiant = search(r"#identifiant'\).val\('(.+?)'\)", text).group(1)

            if not all([self.session_id, self.signature, self.identifiant]):
                raise ValueError("Failed to extract session information from the response.")

            question = search(r'<div class="bubble-body"><p class="question-text" id="question-label">(.+)</p></div>', text)

            if not question:
                raise ValueError("Failed to extract the initial question from the response.")

            self.question = unescape(question.group(1))

            proposition = search(r'<div class="sub-bubble-propose"><p id="p-sub-bubble">([\w\s]+)</p></div>', text)

            if not proposition:
                raise ValueError("Failed to extract the proposition from the response.")

            self.proposition = unescape(proposition.group(1))
            self.progression = 0
            self.step = 0
            self.akitude = "defi.png"
        except Exception as e:
            raise RuntimeError("Failed to start the game.") from e

        return self.session

    def answer(self, answer: str):
        """
        Submits an answer to the current question.
    
        :param answer: The answer to submit. Can be "yes", "no", "i don't know", "probably", or "probably not".
        :type answer: str
        """
        if not answer.lower() in ANSWER_MAP:
            raise InvalidChoiceError(f"Invalid answer: {answer}. Valid answers are: {', '.join(ANSWER_MAP.keys())}")
        answer_id = ANSWER_MAP[answer.lower()]

        if self.win:
            if answer_id == 0:
                return self.choose()
            if answer_id == 1:
                return self.exclude()
            raise InvalidChoiceError("Invalid answer after Akinator has proposed a win. Only 'yes' or 'no' are valid answers at this point.")

        url = f"https://{self.language}.akinator.com/answer"
        data = {
            "step": self.step,
            "progression": self.progression,
            "sid": THEME_IDS[self.theme],
            "cm": str(self.child_mode).lower(),
            "answer": answer_id,
            "step_last_proposition": self.step_last_proposition,
            "session": self.session_id,
            "signature": self.signature
        }

        try:
            response = self.session.post(url, data=data)
            self.__handler(response)
        except Exception as e:
            raise RuntimeError("Failed to submit the answer.") from e

    def back(self):
        """
        Goes back to the previous question in the game.

        .. note::

            This method can only be called if the current step is greater than 0. If the step is 0, it raises a `CantGoBackAnyFurther` exception.        
        """
        if self.step == 0:
            raise CantGoBackAnyFurther()

        url = f"https://{self.language}.akinator.com/cancel_answer"
        data = {
            "step": self.step,
            "progression": self.progression,
            "sid": THEME_IDS[self.theme],
            "cm": str(self.child_mode).lower(),
            "session": self.session_id,
            "signature": self.signature
        }
        self.win = False

        try:
            response = self.session.post(url, data=data)
            self.__handler(response)
        except Exception as e:
            raise RuntimeError("Failed to go back to the previous question.") from e

    def exclude(self):
        """
        Excludes the current proposition from the game.

        .. note::

            This method can only be called after Akinator has proposed a win. If the game is already finished, it will call the `defeat` method.
        """
        if not self.win:
            raise RuntimeError("You can only exclude a proposition after Akinator has proposed a win.")

        if self.finished:
            return self.defeat()

        url = f"https://{self.language}.akinator.com/exclude"
        data = {
            "step": self.step + 1,
            "progression": self.progression,
            "sid": THEME_IDS[self.theme],
            "cm": str(self.child_mode).lower(),
            "session": self.session_id,
            "signature": self.signature,
            "forward_answer": 1
        }
        self.win = False
        self.id_proposition = ""

        try:
            response = self.session.post(url, data=data)
            self.__handler(response)
        except Exception as e:
            raise RuntimeError("Failed to exclude the proposition.") from e

    def choose(self):
        """
        Chooses the current proposition as the answer to the game.

        .. note::

            This method can only be called after Akinator has proposed a win. If the game is already finished, it will raise a `RuntimeError`.
        """
        if not self.win:
            raise RuntimeError("You can only choose a proposition after Akinator has proposed a win.")

        url = f"https://{self.language}.akinator.com/choice"
        data = {
            "step": self.step,
            "sid": THEME_IDS[self.theme],
            "session": self.session_id,
            "signature": self.signature,
            "identifiant": self.identifiant,
            "pid": self.id_proposition,
            "charac_name": self.name_proposition,
            "charac_description": self.description_proposition,
            "pflag_photo": self.flag_photo
        }

        try:
            response = self.session.post(url, data=data, allow_redirects=True)
            if response.status_code not in range(200, 400):
                response.raise_for_status()

            self.finished = True
            self.win = True
            self.akitude = "triomphe.png"
            self.id_proposition = ""
        except Exception as e:
            raise RuntimeError("Failed to choose the proposition.") from e

        try:
            text = response.text
            win_message = unescape(search(r'<span class="win-sentence">(.+?)<\/span>', text).group(1))
            already_played = unescape(search(r'let tokenDejaJoue = "([\w\s]+)";', text).group(1))
            times_selected = search(r'let timesSelected = "(\d+)";', text).group(1)
            times = unescape(search(r'<span id="timesselected"><\/span>\s+([\w\s]+)<\/span>', text).group(1))
            self.question = f"{win_message}\n{already_played} {times_selected} {times}"
        except Exception:
            pass

        self.progression = 100

    def defeat(self):
        """
        Handles the defeat scenario in the game.
        """
        self.finished = True
        self.win = False
        self.akitude = "deception.png"
        self.id_proposition = ""

        questions = {
            "en": "Bravo, you have defeated me !\nShare your feat with your friends.",
            "ar": "أحسنت، لقد هزمتني !\nشارك إنجازك مع أصدقائك.",
            "cn": "太棒了，你打败了我！\n与朋友分享你的成就吧。",
            "de": "Bravo, du hast mich besiegt !\nTeile deinen Erfolg mit deinen Freunden.",
            "es": "¡Bravo, me has derrotado !\nComparte tu hazaña con tus amigos.",
            "fr": "Bravo, tu m'as vaincu  !\nPartage ton exploit avec tes amis.",
            "il": "כל הכבוד, הצלחת להביס אותי !\nשתף את ההישג שלך עם חברים.",
            "it": "Bravo, mi hai sconfitto !\nCondividi la tua impresa con i tuoi amici.",
            "jp": "すごい、あなたは私を倒しました！\nこの偉業を友達と共有しましょう。",
            "kr": "브라보, 당신이 저를 이겼습니다 !\n당신의 업적을 친구들과 공유하세요.",
            "nl": "Bravo, je hebt me verslagen !\nDeel je prestatie met je vrienden.",
            "pl": "Brawo, pokonałeś mnie !\nPodziel się swoim wyczynem ze znajomymi.",
            "pt": "Bravo, você me derrotou !\nCompartilhe sua conquista com seus amigos.",
            "ru": "Браво, ты победил меня !\nПоделись своим достижением с друзьями.",
            "tr": "Bravo, beni yendin !\nBu başarını arkadaşlarınla paylaş.",
            "id": "Hebat, kamu mengalahkanku !\nBagikan pencapaianmu kepada teman-temanmu.",
        }

        self.question = questions[self.language]
        self.progression = 100

    @property
    def confidence(self) -> float:
        """
        Returns the confidence level of the current question.
        """
        return self.progression / 100

    @property
    def theme_id(self) -> int:
        """
        Returns the ID of the current theme.
        """
        return THEME_IDS[self.theme]

    @property
    def theme_name(self) -> str:
        """
        Returns the name of the current theme.
        """
        return "Characters" if self.theme == "c" else "Animals" if self.theme == "a" else "Objects"

    @property
    def akitude_url(self) -> str:
        """
        Returns the URL of the current akitude image.
        """
        return f"https://{self.language}.akinator.com/assets/img/akitudes_670x1096/{self.akitude}"

    def __str__(self):
        if self.win and not self.finished:
            return f"{self.proposition} {self.name_proposition} ({self.description_proposition})"
        return self.question

    def __repr__(self):
        return f"<Akinator Client (Language: {self.language}, Theme: {self.theme_name}, Step: {self.step}, Progression: {self.progression}%)>"

class Akinator(Client):
    """
    A class identical to `Client`, but created for compatibility with the previous version of the library.
    """
