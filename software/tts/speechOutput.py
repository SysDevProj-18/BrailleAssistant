import pyttsx3
import queue
import threading
import time


class SpeechOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self.volume = 1  # from 0.0 to 1.0
        self.rate = 200  # default is 200 wpm
        self.__request_thread_stop = False

    def __enter__(self):
        self.__speech_thread = threading.Thread(target=self.__run)
        self.__speech_thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.__request_thread_stop = True

    def setVolume(self, volume):
        self.volume = volume

    def setRate(self, rate):
        self.rate = rate

    def __run(self):
        while not self.__request_thread_stop:
            if not self.queue.empty():
                text = self.queue.get()
                self.engine.say(text)
                self.engine.runAndWait()
            time.sleep(0.01)

    def speak(self, text):
        self.queue.put(text)


if __name__ == "__main__":
    with SpeechOutput() as tts:
        tts.speak("Hello")
        tts.speak("world")
