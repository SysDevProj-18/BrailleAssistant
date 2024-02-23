from sshkeyboard import listen_keyboard

## DUMMY ##
def text_to_braille(text, contracted):
    return [text, contracted]

def speech_to_text():
    return "<speech>"

def activate_display(braille):
    print(f"activate_display({braille})")
    pass
## /DUMMY ##

# Constants / config
REGULAR_KEYS = ["space"] + list("qwertyuiopasdfghjklzxcvbnm0123456789.:,;!?'\"(){}[]/\\-")
DISPLAY_SIZE = 10


class Main:
    
    def __init__(self):
        self.__keyboard_entry_text = ""
        self.__display_text_alpha = ""
        self.__display_text_contracted = []
        self.__display_text_uncontracted = []

        self.__use_contracted_braille = False
        self.__speak_keypresses = False

        self.__current_display_page = 0
        

    def listen(self):
        listen_keyboard(on_press=self.__on_press, on_release=self.__on_release)


    def __set_display_text(self, text):
        self.__display_text_alpha = text
        self.__display_text_uncontracted = self.__split_into_pages(text_to_braille(text, False))
        self.__display_text_contracted = self.__split_into_pages(text_to_braille(text, True))
        self.__current_display_page = 0
        
        self.__activate_display()

    
    def __split_into_pages(self, braille):
        return [f"__split_into_pages({braille})"] # TODO

    def __activate_display(self):
        activate_display(self.__display_text_contracted if self.__use_contracted_braille else self.__display_text_uncontracted)


    def __on_press(self, key):
        print(f"'{key}' pressed")

        if key in REGULAR_KEYS:
            self.__keyboard_entry_text += key
        elif key == "enter":
            self.__set_display_text(self.__keyboard_entry_text)
            self.__keyboard_entry_text = ""



    def __on_release(self, key):
        pass # TEMP



if __name__ == "__main__":
    Main().listen()