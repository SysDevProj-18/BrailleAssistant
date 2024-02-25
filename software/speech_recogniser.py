#!/usr/bin/env python3

import json
import asyncio
import websockets
import sounddevice as sd


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
            print("EStablsihed microphone")
            print(self.__vosk_uri)
            async with websockets.connect(self.__vosk_uri) as websocket:
                print("ESTablished connection")
                print("SENDING CONFIG")
                await websocket.send(
                    '{ "config" : { "sample_rate" : %d } }' % (device.samplerate)
                )
                print("SENT CONFIG")
                while True:
                    data = await self.__audio_queue.get()
                    print("Say something")
                    await websocket.send(data)
                    text = await websocket.recv()
                    text = json.loads(text)
                    if "result" in text:
                        return text["text"]

    def __init__(
        self, device_id=0, vosk_uri="ws://localhost:2700", sampling_rate=16000
    ):
        self.__vosk_uri = vosk_uri
        self.__sampling_rate = sampling_rate
        self.__device_id = device_id


if __name__ == "__main__":
    sr = SpeechRecogniser()
    text = asyncio.run(sr.listen())
    print(text)
