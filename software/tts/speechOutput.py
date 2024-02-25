import pyttsx3
import queue

class SpeechOutput():

    def __init__(self):

        self.engine = pyttsx3.init()
        self.queue = queue.Queue() 
        self.volume = 1   # from 0.0 to 1.0
        self.rate = 200   # default is 200 wpm

    def setVolume(self, volume):

        self.volume = volume

    def setRate(self, rate):

        self.rate = rate

    def speechEngine(self, text):

        self.engine = pyttsx3.init()

        try:

            self.engine.endLoop()
            del self.engine
            self.engine = pyttsx3.init()

        except:

            pass
            self.engine.startLoop()
            self.engine.say(text)

    def loop(self):

        while True:

            if not self.queue.empty():

                text = self.queue.get()

                self.speechEngine(text)

    def speak(self, text):

        self.queue.put(text)

if __name__ == "__main__":
    tts = SpeechOutput()
    tts.speak("Hello")
    tts.loop()