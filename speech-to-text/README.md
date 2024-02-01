# Speech to Text

## Pre-requisites
`sounddevice, websockets` needs to be installed for this to work. (`pip3 install sounddevice websockets`)
For the Pi (at least on Raspbian OS), Portaudio library is not installed so the following needs to be done:
```
sudo apt-get install libportaudio2
```

A model needs to be installed. Run the following script to install the model:
```
python install-model.py
```


## Run the websocket receiver
`python3 asr_server.py model/en`

## Run the websocket sender
```
./test_microphone.py -u ws://localhost:2700 (windows: $ python test_microphone.py -u ws://localhost:2700)
```
