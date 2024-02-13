import easyocr
import cv2
import os
import keyboard

LANGUAGES = ['ch_sim', 'en']
CAM_PORT = 0
IMG_DIR = 'webcam_image'
IMG_NAME = "webcam_image.png"
TIMEOUT = 30

# Loads OCR language models into memory.
def loadOcrReader(languages):
    return easyocr.Reader(languages, gpu=False)  # Run only once.

# Creates webcame image directory.
def createImageDir(img_dir):
    image_path = os.path.join(os.getcwd(), img_dir)
    os.makedirs(image_path, exist_ok=True)
    return image_path

def waitForSpace(timeout):
    print("Press the space bar to scan your text.")
    keyboard.wait(" ", timeout) # captures anyways after 30 seconds.

def captureImage():
    cap = cv2.VideoCapture(CAM_PORT) # Access webcam.
    _, frame = cap.read() # Capture frame.
    cap.release()
    return frame

# Save captured frame.
def saveImage(image_path, frame):
    image_incl_path = os.path.join(image_path, IMG_NAME)
    cv2.imwrite(image_incl_path, frame)
    return image_incl_path

# Read text using EasyOCR.
def readTxt(reader, image_incl_path):
    txt_result = reader.readtext(image_incl_path)
    txt_lines = [line[1] for line in txt_result]
    txt = ' '.join(txt_lines)
    print(f"Text from {image_incl_path}: {txt}")

def main():
    reader = loadOcrReader(LANGUAGES)
    image_path = createImageDir(IMG_DIR)
    waitForSpace(TIMEOUT)
    image = captureImage()
    image_incl_path = saveImage(image_path, image)
    readTxt(reader, image_incl_path)

if __name__ == "__main__":
    main()