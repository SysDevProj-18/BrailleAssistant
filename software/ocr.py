import easyocr
import cv2
import os
import sshkeyboard
import time

LANGUAGES = ["en"]  # ch_sim for chinese.
CAM_PORT = 0
IMG_DIR = "webcam_image"
IMG_NAME = "webcam_image.png"
TIMEOUT = 30


class VisionRecogniser:
    def debug(self, *args):
        if self.__debug:
            print(f"DEBUG: {args}")

    # Loads OCR language models into memory.
    def loadOcrReader(self, languages):
        return easyocr.Reader(languages, gpu=False)  # Run only once.

    # Creates webcam image directory.
    def createImageDir(self, img_dir):
        image_path = os.path.join(os.getcwd(), img_dir)
        os.makedirs(image_path, exist_ok=True)
        return image_path

    def __press(self, key):
        if key == " ":
            return True
        return False

    def captureImage(self):
        cap = cv2.VideoCapture(CAM_PORT)  # Access webcam.
        _, frame = cap.read()  # Capture frame.
        cap.release()
        return frame

    # Save captured frame.
    def saveImage(self, image_path, frame):
        image_incl_path = os.path.join(image_path, IMG_NAME)
        cv2.imwrite(image_incl_path, frame)
        return image_incl_path

    # Read text using EasyOCR.
    def readTxt(self, reader: easyocr.Reader, image_incl_path):
        txt_result = reader.readtext(image_incl_path, detail=0)
        txt = " ".join(txt_result)
        return txt

    def main(self):
        image_path = self.createImageDir(IMG_DIR)
        image = self.captureImage()
        self.debug("Image captured.", image)
        image_incl_path = self.saveImage(image_path, image)
        self.debug("Image saved.", image_incl_path)
        self.__read_txt = self.readTxt(self.__reader, image_incl_path)
        self.debug("Text read.", self.__read_txt)
        return self.__read_txt

    def __init__(self, debug=False):
        self.__reader = self.loadOcrReader(LANGUAGES)
        self.__read_txt = ""
        self.__debug = debug


if __name__ == "__main__":
    vr = VisionRecogniser()
    text = vr.main()
    print(text)
