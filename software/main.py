from sshkeyboard import listen_keyboard
from Braille import HalfCell, BRAILLE_DICT
from BrailleDisplay import BrailleDisplay

## DUMMY ##
def text_to_braille(text: str, contracted: bool) -> "list[tuple[HalfCell]]":
    return [BRAILLE_DICT[c] for c in text] # TODO

def speech_to_text(): 
    return "speech" # TODO

def text_to_speech(str):
    print(f"text_to_speech({str})") # TODO

def volume_up():
    print("volume_up()") # TODO

def volume_down():
    print("volume_down()") # TODO

## /DUMMY ##

# Constants / config
REGULAR_KEYS = ["space"] + list("qwertyuiopasdfghjklzxcvbnm0123456789.:,;!?'\"(){}[]/\\-")
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
    
    def __init__(self, braille_display):
        self.__keyboard_entry_text = ""
        self.__display_text_alpha = ""
        self.__display_text_contracted = [[]]
        self.__display_text_uncontracted = [[]]

        self.__use_contracted_braille = False
        self.__speak_keypresses = False

        self.__current_display_page = 0

        self.__braille_display = braille_display

        

    def listen(self):
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

    
    def __split_into_pages(self, braille: "list[tuple[HalfCell]]"):
        return [braille] # TODO

    def __activate_display(self):
        self.__braille_display.display(self.__current_display_braille()[self.__current_display_page])


    def __on_press(self, key):
        print(f"'{key}' pressed")

        if self.__speak_keypresses:
            text_to_speech(key)

        if key in REGULAR_KEYS:
            self.__keyboard_entry_text += key
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
            text_to_speech(self.__display_text_alpha)
        elif key == KEY_MICROPHONE:
            self.__set_display_text(speech_to_text())
        elif key == KEY_PREVIOUS_PAGE:
            if self.__current_display_page != 0:
                self.__current_display_page -= 1
                self.__activate_display()
        elif key == KEY_NEXT_PAGE:
            if self.__current_display_page != len(self.__current_display_braille()):
                self.__current_display_page -= 1
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
        with BrailleDisplay() as display:
            Main(display).listen()
    except KeyboardInterrupt:
        print("exiting")