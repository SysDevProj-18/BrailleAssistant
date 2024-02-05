# install https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
# unzip and move to model

import os
import requests
import zipfile
def install_model():
    print("Installing model")
    r = requests.get("https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
    with open("model.zip", "wb") as code:
        code.write(r.content)
    # rename to en
    with zipfile.ZipFile("model.zip", 'r') as zip_ref:
        zip_ref.extractall("model")
    os.remove("model.zip")
    # rename model/en-us-0.15 to model/en
    os.rename("model/vosk-model-small-en-us-0.15", "model/en")

def __main__():
    install_model()

if __name__ == "__main__":
    __main__()
