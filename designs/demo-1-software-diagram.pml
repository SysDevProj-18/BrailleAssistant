@startuml
|#AntiqueWhite|Websocket Server|
:Load VOSK model;
:Assign various VOSK paramters (sample rate, etc);
:Start VOSK Server;
:Accept incoming Websocket connections;
|Main Module|
:Establish Microphone Connection;
:Establish Websocket Connection;
:Wait for when speech to braille to be activated;
|Websocket Server|
:Process Audio;
|Main Module|
:Receive transcription;
|#AntiqueWhite|Text-to-Braile module|
:Process text;
|Main Module|
:Receive Braille equivalent of the text;
:Receive Display Braille;
@enduml
