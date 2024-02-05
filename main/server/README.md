# Speech to Text

## Pre-requisites
`sounddevice, websockets` needs to be installed for this to work. (`pip3 install sounddevice websockets`)
For the Pi (at least on Raspbian OS), Portaudio library is not installed so the following needs to be done:
```
sudo apt-get install libportaudio2
```

A model needs to be installed. Run the following script to install the model:
```
python install_model.py
```

## Running the Server
```bash
./asr_server.py model/en
```

Example:
```bash
python test_microphone.py -u ws://localhost:2700
hello -> ⠓⠑⠇⠇⠕
apple -> ⠁⠏⠏⠇⠑
nash -> ⠝⠁⠩
```
