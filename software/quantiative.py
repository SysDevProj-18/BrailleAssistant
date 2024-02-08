#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import websockets
import logging
import sounddevice as sd
import argparse
import csv
from demo1 import text_to_braille

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

async def run_test(websocket, file, expected_word, num_samples=1):
    data_count = 0
    print(f"Pronounce the word '{expected_word}'")
    while data_count < num_samples:
        data = await audio_queue.get()
        await websocket.send(data)
        text = await websocket.recv()
        text = json.loads(text)
        if 'result' in text:
            conf = text['result'][0]['conf']
            word = text['result'][0]['word']
            print(f'{word} -> {text_to_braille(word)}')
            csv.writer(file).writerow([expected_word, word, conf])
            data_count += 1

async def main(file):
    global args
    global loop
    global audio_queue

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    parser = argparse.ArgumentParser(description="ASR Server",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     parents=[parser])
    parser.add_argument('-u', '--uri', type=str, metavar='URL',
                        help='Server URL', default='ws://localhost:2700')
    parser.add_argument('-d', '--device', type=int_or_str,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
    args = parser.parse_args(remaining)
    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue()

    logging.basicConfig(level=logging.INFO)

    # Establish WebSocket connection
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 4000, device=args.device, dtype='int16', channels=1, callback=callback) as device:
        async with websockets.connect(args.uri) as websocket:
            await websocket.send('{ "config" : { "sample_rate" : %d } }' % (device.samplerate))
            while True:
                expected_word = input("Enter the expected word for this speech: ")
                num_samples = int(input("Enter the number of samples you would like to process: "))
                await run_test(websocket, file, expected_word, num_samples)

                # Ask if the user wants to continue or exit
                choice = input("Do you want to continue with another test? (yes/no): ").lower()
                if choice != 'yes':
                    break

if __name__ == '__main__':
    with open('results.csv', 'a') as f:
        asyncio.run(main(f))

