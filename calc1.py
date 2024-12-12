from tkinter import *
from PIL import Image, ImageGrab
import os
import numpy as np
import pyautogui
import easyocr
import cv2
import time

recognized_texts = []
# Function to read text at specific coordinates on the screen
def read_text_at_coordinates(top_left_x, top_left_y, width, height):
    global recognized_texts
    try:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        cropped_image_np = screenshot_np[top_left_y:top_left_y + height, top_left_x:top_left_x + width]
        cropped_image = Image.fromarray(cropped_image_np)
        cropped_image.save('cropped_image.png')
        cropped_image = cropped_image.convert('L')
        reader = easyocr.Reader(['en'])
        result = reader.readtext(np.array(cropped_image))
        for(_, text, _) in result:
            recognized_texts.append(text)
        return(recognized_texts)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def recognize_text():
    l = []
    text = read_text_at_coordinates(70, 50, 1100, 800)
    if text:
        label.config(text=", ".join(text))
        print(text)
    else:
        label.config(text="No text recognized or an error occurred.")

# Create the main window
window = Tk()
window.title("Handwriting Calculator")

# Label to display recognized text
label = Label(window, text="")
label.grid(row=1, column=0, columnspan=2)

# Create a canvas for drawing
last_x, last_y = None, None
canvas = Canvas(window, width=1200, height=800, bg='black', cursor='cross')
canvas.grid(row=0, column=0, pady=2, columnspan=2)

# Function to activate drawing on the canvas
def activate_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    
# Function to draw on the canvas
def draw(event):
    global last_x, last_y
    canvas.create_line((last_x, last_y, event.x, event.y), width=5, fill='white', capstyle=ROUND, smooth=TRUE)
    last_x, last_y = event.x, event.y

# Bind drawing events to the canvas
canvas.bind("<Button-1>", activate_draw)
canvas.bind("<B1-Motion>", draw)

# Button to trigger text recognition
button_save = Button(window, text="Recognize", command=recognize_text)
button_save.grid(row=2, column=0)

# Button to clear the canvas
button_clear = Button(window, text="Clear", command=lambda: canvas.delete("all"))
button_clear.grid(row=2, column=1)


# Run the Tkinter event loop
window.mainloop()