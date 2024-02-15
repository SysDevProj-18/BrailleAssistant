import threading 
import time
import queue
import numpy as np 
import speech_recognition as sr
from faster_whisper import WhisperModel
from braillepy import text_to_braille
class SpeechRecognition:
    def __init__(self, model="small.en", device="cpu", log_time=False):
        self.audio_model = WhisperModel(model, device, compute_type="int8")
        self.source = sr.Microphone(sample_rate=16000, device_index=None)
        self.recorder = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.result_queue: "queue.Queue[str]" = queue.Queue()
        self.log_time = log_time
    def __callback(self,_, audio: sr.AudioData):
        print("Audio data received")
        data = audio.get_raw_data()
        self.audio_queue.put_nowait(data)
    def __get_all_audio(self):
        audio = bytes()
        while not self.audio_queue.empty():
            audio += self.audio_queue.get_nowait()
        data = sr.AudioData(audio, sample_rate=16000, sample_width=2).get_raw_data()
        
        # faster_whisper wants an NDArray
        return np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
    def __transcribe(self):
        audio_data = self.__get_all_audio()
        if len(audio_data) == 0:
            return
        predicted_text = ''
        time_start = time.time()
        segments, info = self.audio_model.transcribe(audio_data)
        time_end = time.time()
        print(f"Time taken: {time_end - time_start}, audio length: {len(audio_data) / 16000}")
        for segment in segments:
            predicted_text += segment.text
        self.result_queue.put_nowait(predicted_text)
    def __transcribe_loop(self):
        while True:
            self.__transcribe()
    def listen_loop(self):
        self.recorder.listen_in_background(self.source, self.__callback, phrase_time_limit=None)
        print("Listening...")
        threading.Thread(target=self.__transcribe_loop, daemon=True).start()

        while True:
            yield self.result_queue.get()

if __name__ == "__main__":
    recognizer = SpeechRecognition()
    for text in recognizer.listen_loop():
        if text != '':
            print(f'{text} -> {text_to_braille(text)}')
