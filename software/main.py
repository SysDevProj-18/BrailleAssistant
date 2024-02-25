from sshkeyboard import listen_keyboard
from Braille import HalfCell, BRAILLE_DICT
from BrailleDisplay import BrailleDisplay
from speech_recogniser import SpeechRecogniser
from tts.speechOutput import SpeechOutput
import asyncio


## DUMMY ##
def text_to_braille(text: str, contracted: bool) -> "list[tuple[HalfCell]]":
    return [BRAILLE_DICT[c] for c in text] # TODO

def speech_to_text(): 
    sr = SpeechRecogniser()
    text = asyncio.run(sr.listen())
    return text

def volume_up():
    print("volume_up()") # TODO

def volume_down():
    print("volume_down()") # TODO

## /DUMMY ##

## DEBUG ##

def cell_to_string(left: HalfCell, right: HalfCell):
    return chr(10240 + left + right * 8)

def cells_to_string(cells: "list[tuple[HalfCell, HalfCell]]"):
    return "".join(cell_to_string(*cell) for cell in cells)

def pages_to_string(pages: "list[list[tuple[HalfCell, HalfCell]]]"):
    return " / ".join(f"{cells_to_string(page)} ({len(page)} cells)" for page in pages)

## /DEBUG ##

# Constants / config
REGULAR_KEYS = list("qwertyuiopasdfghjklzxcvbnm0123456789.:,;!?'\"(){}[]/\\-")
KEY_SPACE = "space"
KEY_BACKSPACE_TEXT_ENTRY = "backspace"
KEY_CLEAR_TEXT_ENTRY = "delete"
KEY_SUBMIT_TEXT_ENTRY = "enter"
KEY_SPEAK_KEYPRESS_ON = "f2"
KEY_SPEAK_KEYPRESS_OFF = "f3"
KEY_SPEAK_STORED = "f4"
KEY_MICROPHONE = "f5"
KEY_PREVIOUS_PAGE = "left"
KEY_NEXT_PAGE = "right"
KEY_UNCONTRACTED_BRAILLE = "f11"
KEY_CONTRACTED_BRAILLE = "f12"
KEY_VOLUME_UP = "pagedown"
KEY_VOLUME_DOWN = "pageup"
DISPLAY_SIZE = 10
BRAILLE_SPACE = (HalfCell.NO_DOT, HalfCell.NO_DOT)


class Main:
    
    def __init__(self, braille_display, text_to_speech):
        self.__keyboard_entry_text = ""
        self.__display_text_alpha = ""
        self.__display_text_contracted = [[]]
        self.__display_text_uncontracted = [[]]

        self.__use_contracted_braille = False
        self.__speak_keypresses = False

        self.__current_display_page = 0

        self.__braille_display = braille_display
        self.__text_to_speech = text_to_speech

        

    def run(self):
        listen_keyboard(on_press=self.__on_press, on_release=self.__on_release)

    
    def __current_display_braille(self):
        return self.__display_text_contracted if self.__use_contracted_braille else self.__display_text_uncontracted


    def __set_display_text(self, text: str):
        print(f"old display text: \"{self.__display_text_alpha}\"; new display text: \"{text}\"")

        self.__display_text_alpha = text
        self.__display_text_uncontracted = self.__split_into_pages(text_to_braille(text, False))
        self.__display_text_contracted = self.__split_into_pages(text_to_braille(text, True))
        self.__current_display_page = 0


        
        self.__activate_display()

    
    def __split_into_words(self, to_split: "list[tuple[HalfCell]]"):
        words = []
        current_word = []
        for cell in to_split:
            if cell == BRAILLE_SPACE:
                if current_word != []:
                    words.append(current_word)
                    current_word = []
            else:
                current_word.append(cell)
        words.append(current_word) # final word

        return words


    def __split_into_pages(self, to_split: "list[tuple[HalfCell]]"):
        print(f"splitting {cells_to_string(to_split)} into pages...")
        words = self.__split_into_words(to_split)
        print(f"...words are {pages_to_string(words)}...")

        if words == [[]]:
            print(f"...no words; returning empty page [[]].")
            return [[]]
        

        pages = []
        current_page = []

        for word in words:
            if len(current_page) == 0 and len(word) <= DISPLAY_SIZE:
                current_page += word # no need for space at start
            elif len(current_page) + 1 + len(word) <= DISPLAY_SIZE: # can fit on existing page
                current_page.append(BRAILLE_SPACE)
                current_page += word
            else:
                if current_page != []:
                    pages.append(current_page) # page finished
                if len(word) <= DISPLAY_SIZE: # word can fit in display
                    current_page = word # word goes to start of next page
                else: # we have to split the word up
                    new_pages = []
                    for i in range(0, len(word), DISPLAY_SIZE):
                        new_pages.append(word[i:i+DISPLAY_SIZE])
                    pages += new_pages[:-1] # add whole pages for parts of the word
                    current_page = new_pages[-1] # final part can go on start of next page
        
        if current_page != []:
            pages.append(current_page) # final page
        
        print(f"...pages are {pages_to_string(pages)}.")

        return pages

    def __activate_display(self):
        print(f"activating display with page {self.__current_display_page} ({cells_to_string(self.__current_display_braille()[self.__current_display_page])})")
        self.__braille_display.display(self.__current_display_braille()[self.__current_display_page])


    def __on_press(self, key):
        print(f"'{key}' pressed")

        if self.__speak_keypresses:
            self.__text_to_speech.speak(key)

        if key in REGULAR_KEYS:
            self.__keyboard_entry_text += key
        if key == KEY_SPACE:
            self.__keyboard_entry_text += " "
        elif key == KEY_SUBMIT_TEXT_ENTRY:
            self.__set_display_text(self.__keyboard_entry_text)
            self.__keyboard_entry_text = ""
        elif key == KEY_BACKSPACE_TEXT_ENTRY:
            self.__keyboard_entry_text = self.__keyboard_entry_text[:-1]
        elif key == KEY_CLEAR_TEXT_ENTRY:
            self.__keyboard_entry_text = ""
        elif key == KEY_SPEAK_KEYPRESS_ON:
            self.__speak_keypresses = True
        elif key == KEY_SPEAK_KEYPRESS_OFF:
            self.__speak_keypresses = False
        elif key == KEY_SPEAK_STORED:
            self.__text_to_speech.speak(self.__display_text_alpha)
        elif key == KEY_MICROPHONE:
            self.__set_display_text(speech_to_text())
        elif key == KEY_PREVIOUS_PAGE:
            if self.__current_display_page != 0:
                self.__current_display_page -= 1
                self.__activate_display()
        elif key == KEY_NEXT_PAGE:
            if self.__current_display_page != len(self.__current_display_braille()):
                self.__current_display_page += 1
                self.__activate_display()
        elif key == KEY_UNCONTRACTED_BRAILLE:
            self.__use_contracted_braille = False
            self.__current_display_page = 0
            self.__activate_display()
        elif key == KEY_CONTRACTED_BRAILLE:
            self.__use_contracted_braille = True
            self.__current_display_page = 0
            self.__activate_display()
        elif key == KEY_VOLUME_DOWN:
            volume_down()
        elif key == KEY_VOLUME_UP:
            volume_up()

    def __on_release(self, key):
        pass # TEMP



if __name__ == "__main__":
    try:
        with BrailleDisplay() as display, SpeechOutput() as tts:
            Main(display, tts).run()
    except KeyboardInterrupt:
        print("exiting")