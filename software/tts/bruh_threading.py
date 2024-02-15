import pyttsx3
import keyboard
import threading
import queue

def monitorKeyboard(text_queue):
    print("Press ESC to exit")
    fullWord = ""

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            text_queue.put(event.name)

def speak_text(text):
    engine = pyttsx3.init()
    try:
        engine.endLoop()
        del engine
        engine = pyttsx3.init()
    except:
        pass
        engine.startLoop()
        engine.say(text)
def loop(text_queue):
    while True:
        if not text_queue.empty():
            text = text_queue.get()
            if text == "esc":
                break
            else:
                speak_text(text)
def main():
    text_queue = queue.Queue()  # Queue to communicate between threads
    
    # Create threads for monitoring keyboard and speaking text
    keyboard_thread = threading.Thread(target=monitorKeyboard, args=(text_queue,))
    loop_thrad = threading.Thread(target=loop, args=(text_queue,))

    # Start both threads
    keyboard_thread.start()
    loop_thrad.start()

if __name__ == "__main__":
    main()

