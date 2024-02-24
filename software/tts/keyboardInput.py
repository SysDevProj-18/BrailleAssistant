# THIS CODE DOESN'T USE THREADING SO ITS NOT VERY USEFUL BUT ILL KEEP IT HERE FOR NOW ~ FL0W

import pyttsx3
import keyboard

def monitorKeyboard():

    print("press ESC to exit")
    engine = pyttsx3.init()
    fullWord = ""

    while True:

        event = keyboard.read_event()
        engine.stop()

        print(event.name)
        
        if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':

            break

        elif event.event_type == keyboard.KEY_DOWN and event.name == 'enter':

            text = fullWord
            fullWord = ""

        else:

            fullWord += event.name
            text = event.name

        engine.say(text)
        engine.runAndWait()

monitorKeyboard()


