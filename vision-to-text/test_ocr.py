import easyocr
import os

image_path = os.path.join(os.getcwd(),'images')
os.chdir(image_path)
reader = easyocr.Reader(['ch_sim','en'], gpu=False) # Run only once to load the model into memory.

fileName = str(input("Enter filename: "))
txt_result = reader.readtext(fileName)

txt_lines = [line[1] for line in txt_result]
txt = ' '.join(txt_lines)
print(txt)