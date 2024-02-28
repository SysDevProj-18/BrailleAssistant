#!/usr/bin/env python3

import json
import asyncio
import websockets
import sounddevice as sd
import csv


class SpeechRecogniser:
    def __callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        self.__loop.call_soon_threadsafe(self.__audio_queue.put_nowait, bytes(indata))

    async def listen(self):
        self.__loop = asyncio.get_running_loop()
        self.__audio_queue = asyncio.Queue()
        with sd.RawInputStream(
            samplerate=self.__sampling_rate,
            blocksize=4000,
            device=self.__device_id,
            dtype="int16",
            channels=1,
            callback=self.__callback,
        ) as device:
            print(self.__vosk_uri)
            async with websockets.connect(self.__vosk_uri) as websocket:
                await websocket.send(
                    '{ "config" : { "sample_rate" : %d } }' % (device.samplerate)
                )
                while True:
                    data = await self.__audio_queue.get()
                    await websocket.send(data)
                    text = await websocket.recv()
                    text = json.loads(text)
                    if "result" in text:
                        return (text["text"], text["result"][0]["conf"])

    def __init__(
        self, device_id=0, vosk_uri="ws://localhost:2700", sampling_rate=16000
    ):
        self.__vosk_uri = vosk_uri
        self.__sampling_rate = sampling_rate
        self.__device_id = device_id


if __name__ == "__main__":
    with open("results.csv", "a") as f:
        sr = SpeechRecogniser(sampling_rate=44100, device_id=1)
        expected_word = input("Enter the expected word for this speech: ")
        num_samples = int(
            input("Enter the number of samples you would like to process: ")
        )
        name = input("Enter your name: ")
        counter = 0
        while True:
            print(f"Say the word {expected_word}")
            tup = asyncio.run(sr.listen())
            csv.writer(f).writerow([name, expected_word, tup[0], tup[1]])
            counter += 1
            if counter == num_samples:
                s = input("Would you like to continue? (y/n): ")
                if s == "n":
                    break
                else:
                    expected_word = input("Enter the expected word for this speech: ")
                    num_samples = int(
                        input("Enter the number of samples you would like to process: ")
                    )
                    counter = 0
