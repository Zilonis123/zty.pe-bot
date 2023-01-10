import pyautogui
from time import sleep, perf_counter
# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm
import re
import pytesseract
import os
# importing OpenCV
import cv2
  
from PIL import ImageGrab


# PATH TO TESSERACT
tesseract = '<< PATH TO TESSERACT EXE >>'

# clear the console
os.system("cls")

# Get the game location
input("Place your mouse cursor over the top left corner...")
sleep(1.5)

top_left = pyautogui.position()

input("Now place it over the bottom right corner")
sleep(1.5)

bottom_right = pyautogui.position()
game_reg = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
input("Press enter to start (you have to already be inside the game)")
sleep(1)


def imToString(reg):
        # Path of tesseract executable
        pytesseract.pytesseract.tesseract_cmd = tesseract
        # ImageGrab-To capture the screen image in a loop. 
        # Bbox used to capture a specific area.
        cap = ImageGrab.grab(bbox=reg)

        # Converted the image to monochrome for it to be easily 
        # read by the OCR and obtained the output String.
        tesstr = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), 
                lang ='eng')
        return tesstr


special_characters = "‘!@#$%^&*()-+?_=,<>/0123456789"
# game loop
while (True):

        # start measuring time
        t_0 = perf_counter()

        # get the screen
        sString = imToString(game_reg)

        words = sString.split("\n")
        for word in words:
                w = word.split(" ")
                if w[0] == "WAVE":
                        # in the case that we detected a new wave STOP
                        break
                if len(w) > 0:
                        for wo in w:
                                # remove symbols from word
                                wo = re.sub('\W+','', wo)
                                # type the word
                                pyautogui.write(wo, interval=0.05)
                        break
        
        # log the time in the console
        # clear the console
        os.system("cls")
        
        t_2 = perf_counter()
        ms = (t_2-t_0) * 10**6
        print(f"Elapsed time: {ms:.03f}ms")
        