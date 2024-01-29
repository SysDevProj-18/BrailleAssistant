# Speech to Text
To run it, Docker needs to be installed. Aftewards run the following command:
```
docker-compose up -d 
```
The `-d` flag is optional and runs the container in the background.

Afterwards there's a couple of ways to test it out. For now I just cloned one of vosk's repos which has 
a bunch of useful scripts. Here's some examples:

## Run websocket which will listen to the microphone
```
cd vosk-server/websocket/
pip3 install sounddevice
./test_microphone.py -u ws://localhost:2700
```

## Run websocket which will listen to a file
```
cd vosk-server/websocket/
./test.py test16k.wav
```

