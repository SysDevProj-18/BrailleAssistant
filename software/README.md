# SDP Software
To run the software, you need to have Python installed, and the following dependencies:
- requests
- vosk
- websockets
- sounddevice
- asyncio

VOSK server needs to be running in the background. To run the server, check the README in the server directory.

Afterwards you can run the client by running the following command:
```bash
python test_microphone.py -u ws://localhost:2700
```
And now it will capture your voice and translate the first word (if you say multiple words in a row). 

