# SDP Software

## VOSK Model
To run the software, you need to have Python installed, and the following dependencies:
- requests
- vosk
- websockets
- sounddevice
- asyncio
- pyttsx3
- sshkeyboard
- lgpio
- gpiozero
- regex

VOSK server needs to be running in the background. To run the server, check the README in the server directory.

Afterwards, you can run the main.py file to start the software.
```bash 
python main.py
```

(on the pi, you will need to install the packages globally which can be done by running the following command
```bash
pip install --break-system-packages ...
```
for some reason gpiozero does not play nice with virtual environments)


## Whisper Moel (Experimental)
Instructions for how to run the whisper model.
Go into the whisper directory and run the following command:
```bash
pip install -r requirements.txt
```
Afterwards you can run the client by running the following command:
```bash
python main.py
```


On the Pi 
PyAudio has the following dependencies:
```bash
sudo apt install portaudio19-dev python3-pyaudio
```

