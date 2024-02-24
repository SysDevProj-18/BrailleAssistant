# THIS IS SOME F'D UP CODE BUT IT MIGHT PROVE TO BE USEFUL SO IM KEEPING IT HERE FOR NOW ~ FL0W

import keyboard
import threading
import speechOutput

def monitorKeyboard():

    print("Press ESC to exit")
    speechOutput.say("Press ESC to exit")

    while True:

        event = keyboard.read_event()


        # here you can define all of the hotkeys using 'if event.event_type == keyboard.KEY_DOWN and event.name == whatever' or 'event.name in array'
        if event.event_type == keyboard.KEY_DOWN:
            
            print(event.name)
            speechOutput.stop_speaker()
            speechOutput.say(event.name)

def main():
    
    monitorKeyboard()
    #keyboard_thread = threading.Thread(target=monitorKeyboard, args=(text_queue,))
    #keyboard_thread.start() 

if __name__ == "__main__":

    main()

