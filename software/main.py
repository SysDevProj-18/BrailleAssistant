import enum
from sshkeyboard import listen_keyboard
from data_structures import HalfCell, _BRAILLE_DICT
from constants import Constants
from BrailleDisplay import BrailleDisplay
from speech_recogniser import SpeechRecogniser
from ocr import VisionRecogniser
from tts.speechOutput import SpeechOutput
from text_to_braille import BrailleTranslator
import asyncio
import os
import argparse
from game import Game


def speech_to_text():
    sr = SpeechRecogniser()
    text = asyncio.run(sr.listen())
    return text


def volume_up():
    print("volume_up()")  # TODO


def volume_down():
    print("volume_down()")  # TODO


## /DUMMY ##


def image_to_text(vr: VisionRecogniser, debug=False):
    text = vr.main()
    return text


## DEBUG ##


def cell_to_string(left: HalfCell, right: HalfCell):
    return chr(10240 + left + right * 8)


def cells_to_string(cells: "list[tuple[HalfCell, HalfCell]]"):
    return "".join(cell_to_string(*cell) for cell in cells)


def pages_to_string(pages: "list[list[tuple[HalfCell, HalfCell]]]"):
    return " / ".join(f"{cells_to_string(page)} ({len(page)} cells)" for page in pages)


class MODE(enum.Enum):
    DEFAULT = 0
    CAMERA = 1
    GAME = 2


class Main:
    def debug(self, *args):
        if self.__debug:
            print(f"DEBUG: {args}")

    def __init__(
        self, braille_display: BrailleDisplay, text_to_speech: SpeechOutput, debug=False
    ):
        self.__keyboard_entry_text = ""
        self.__display_text_alpha = ""
        self.__display_text_contracted = [[]]
        self.__display_text_uncontracted = [[]]

        self.__use_contracted_braille = False
        self.__speak_keypresses = False

        self.__current_display_page = 0

        self.__braille_display = braille_display
        self.__text_to_speech = text_to_speech
        self.__bt = BrailleTranslator()

        self.__game = None

        self.__debug = debug
        self.__mode = MODE.DEFAULT
        self.__vr = VisionRecogniser(debug)

    def run(self):
        listen_keyboard(on_press=self.__on_press, on_release=self.__on_release)

    def __current_display_braille(self):
        self.debug(f"Contracted: {self.__use_contracted_braille}")
        return (
            self.__display_text_contracted
            if self.__use_contracted_braille
            else self.__display_text_uncontracted
        )

    def __set_display_text(self, text: str):
        print(
            f'old display text: "{self.__display_text_alpha}"; new display text: "{text}"'
        )

        self.__display_text_alpha = text
        self.__display_text_uncontracted = self.__split_into_pages(
            self.__bt.translate(text, False)
        )
        self.__display_text_contracted = self.__split_into_pages(
            self.__bt.translate(text, True)
        )
        self.__current_display_page = 0

        self.__activate_display()

    def __split_into_words(self, to_split: "list[tuple[HalfCell, HalfCell]]"):
        words = []
        current_word = []
        for cell in to_split:
            if cell == Constants.BRAILLE_SPACE:
                if current_word != []:
                    words.append(current_word)
                    current_word = []
            else:
                current_word.append(cell)
        words.append(current_word)  # final word

        return words

    def __split_into_pages(self, to_split: "list[tuple[HalfCell, HalfCell]]"):
        print(f"splitting {cells_to_string(to_split)} into pages...")
        words = self.__split_into_words(to_split)
        print(f"...words are {pages_to_string(words)}...")

        if words == [[]]:
            print(f"...no words; returning empty page [[]].")
            return [[]]

        pages = []
        current_page = []

        for word in words:
            if len(current_page) == 0 and len(word) <= Constants.DISPLAY_SIZE:
                current_page += word  # no need for space at start
            elif (
                len(current_page) + 1 + len(word) <= Constants.DISPLAY_SIZE
            ):  # can fit on existing page
                current_page.append(Constants.BRAILLE_SPACE)
                current_page += word
            else:
                if current_page != []:
                    pages.append(current_page)  # page finished
                if len(word) <= Constants.DISPLAY_SIZE:  # word can fit in display
                    current_page = word  # word goes to start of next page
                else:  # we have to split the word up
                    new_pages = []
                    for i in range(0, len(word), Constants.DISPLAY_SIZE):
                        new_pages.append(word[i : i + Constants.DISPLAY_SIZE])
                    pages += new_pages[:-1]  # add whole pages for parts of the word
                    current_page = new_pages[
                        -1
                    ]  # final part can go on start of next page

        if current_page != []:
            pages.append(current_page)  # final page

        print(f"...pages are {pages_to_string(pages)}.")

        return pages

    def __activate_display(self):
        print(f"length of display: {(self.__current_display_braille())}")
        print(
            f"activating display with page {self.__current_display_page} ({cells_to_string(self.__current_display_braille()[self.__current_display_page])})"
        )
        self.__braille_display.display(
            self.__current_display_braille()[self.__current_display_page]
        )

    def __on_press(self, key):
        print(f"'{key}' pressed")

        if self.__speak_keypresses:
            self.debug(f"speak keypress: {key}")
            self.__text_to_speech.speak(key)

        print(f"current mode: {self.__mode}")
        if self.__mode == MODE.CAMERA:
            if key == Constants.KEY_SPACE:
                img = image_to_text(self.__vr, self.__debug)
                print(f"OCR: {img}")
                pass
        else:

            if self.__mode == MODE.GAME:
                if key == Constants.KEY_GAME_OPTIONS:
                    self.__game.sendInput(key)
                    return
                elif key == Constants.KEY_MICROPHONE:
                    self.__game.sendInput(speech_to_text())
                    return
                elif key == Constants.KEY_GAME:
                    self.__game.sendInput("#")
                    return
            if key in Constants.REGULAR_KEYS:
                self.__keyboard_entry_text += key
            if key == Constants.KEY_SPACE:
                self.__keyboard_entry_text += " "
            elif key == Constants.KEY_SUBMIT_TEXT_ENTRY:
                self.__set_display_text(self.__keyboard_entry_text)
                self.__keyboard_entry_text = ""
            elif key == Constants.KEY_BACKSPACE_TEXT_ENTRY:
                self.__keyboard_entry_text = self.__keyboard_entry_text[:-1]
            elif key == Constants.KEY_CLEAR_TEXT_ENTRY:
                self.__keyboard_entry_text = ""
            elif key == Constants.KEY_SPEAK_KEYPRESS_ON:
                self.debug("speak keypresses on")
                self.__speak_keypresses = True
            elif key == Constants.KEY_SPEAK_KEYPRESS_OFF:
                self.__speak_keypresses = False
            elif key == Constants.KEY_SPEAK_STORED:
                self.__text_to_speech.speak(self.__display_text_alpha)
            elif key == Constants.KEY_MICROPHONE:
                self.__set_display_text(speech_to_text())
            elif key == Constants.KEY_CAMERA:
                self.__mode = MODE.CAMERA
                return
            elif key == Constants.KEY_GAME:  
                self.__mode = MODE.GAME
                self.__game = Game(self.__text_to_speech.speak, self.__set_display_text)
                return
            elif key == Constants.KEY_PREVIOUS_PAGE:
                if self.__current_display_page != 0:
                    self.__current_display_page -= 1
                    self.__activate_display()
            elif key == Constants.KEY_NEXT_PAGE:
                if self.__current_display_page != len(self.__current_display_braille()):
                    self.__current_display_page += 1
                    self.__activate_display()
            elif key == Constants.KEY_UNCONTRACTED_BRAILLE:
                self.__use_contracted_braille = False
                self.__current_display_page = 0
                self.__activate_display()
            elif key == Constants.KEY_CONTRACTED_BRAILLE:
                self.__use_contracted_braille = True
                self.__current_display_page = 0
                self.__activate_display()
            elif key == Constants.KEY_VOLUME_DOWN:
                volume_down()
            elif key == Constants.KEY_VOLUME_UP:
                volume_up()
            self.__mode = MODE.DEFAULT

    def __on_release(self, key):
        pass  # TEMP


if __name__ == "__main__":
    # flags
    parser = argparse.ArgumentParser(description="BrailleEd program")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run without GPIO (for testing)",
    )
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()
    if not args.local:
        os.environ["GPIOZERO_PIN_FACTORY"] = os.environ.get(
            "GPIOZERO_PIN_FACTORY", "lgpio"
        )
    else:
        os.environ["GPIOZERO_PIN_FACTORY"] = os.environ.get(
            "GPIOZERO_PIN_FACTORY", "mock"
        )
    try:
        with BrailleDisplay() as display, SpeechOutput() as tts:
            Main(display, tts, args.debug).run()
    except KeyboardInterrupt:
        print("exiting")