import pyttsx3
import queue
import threading
import time


class SpeechOutput:
    def __init__(self):
        #self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        #self.volume = 1  # from 0.0 to 1.0
        #self.rate = 200  # default is 200 wpm
        self.__request_thread_stop = False

    def __enter__(self):
        self.__speech_thread = threading.Thread(target=self.__run)
        self.__speech_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__request_thread_stop = True

    #def setVolume(self, volume):
    #    self.volume = volume

    #def setRate(self, rate):
    #    self.rate = rate

    def __run(self):
        #self.engine.startLoop(False)
        while not self.__request_thread_stop:
            #print(self.engine.isBusy())
            if not self.queue.empty():
                text = self.queue.get()
                #print(text)

                pyttsx3.speak(text)
                
                #self.engine.say(text)
                #self.engine.iterate()
                #print("spoken")
                #self.engine.stop()
            
            time.sleep(0.0001)
        print("DONE")
        #self.engine.endLoop()


    def speak(self, text):
        self.queue.put(text)


if __name__ == "__main__":
    with SpeechOutput() as tts:
        tts.speak("Hello")
        tts.speak("world")
        input("press enter to exit")
