from tkinter import *
from PIL import Image, ImageGrab
import os
import numpy as np
import pyautogui
import easyocr
import cv2
import time

n = 0
recognized_texts = []

# Function to read text at specific coordinates on the screen
def read_text_at_coordinates(top_left_x, top_left_y, width, height):
    global recognized_texts
    recognized_texts = []
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
            for char in text:
                recognized_texts.append(char)
        return(recognized_texts)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def perform_task(text):
    global n
    opr = ''
    equalto = ''
    fvalue = 0
    svalue = 0
    result = 0
    found_operator = False

    print(f"Processing text: {text}")

    for i in text:
        i = i.strip()
        if i.isdigit():
            if not found_operator:
                fvalue = fvalue * 10 + int(i)
            else:
                svalue = svalue * 10 + int(i)
        elif i in ['+', '-', '*', '/', '%', '^']:
            opr = i
            found_operator = True

        elif(i == '='):
            global equal_coords, last_x, last_y
            equal_coords = (last_x, last_y)  # Save coordinates of '=' sign
            print(last_x)
            print(last_y)
            break
            
    fvalue = int(fvalue)
    svalue = int(svalue)
    if opr == '+':
        result = fvalue + svalue
    elif opr == '-':
        result = fvalue - svalue
    elif opr == '*':
        result = fvalue * svalue
    elif opr == '/':
        result = fvalue / svalue
    elif opr == '%':
        result = fvalue % svalue
    elif opr == '^':
        result = fvalue ** svalue
            
    print(fvalue)
    print(svalue)
    print(opr)
    print(result)
    canvas.create_text(last_x + 100, last_y, text=result, font=('Arial Narro]=', 80), fill='white')
    n += 1
    #global recognized_texts, last_x, last_y
    recognized_texts = []  # Clear the recognized texts list
    last_x, last_y = None, None  # Reset drawing coordinates
    label.config(text="")
    

def recognize_text():
    if(n == 0):
        text = read_text_at_coordinates(70, 50, 1100, 800)
    elif(n == 1):
        text = read_text_at_coordinates(70, 316, 1100, 534)
    elif(n == 2):
        text = read_text_at_coordinates(70, 582, 1100, 268)
    if text:
        label.config(text=", ".join(text))
        perform_task(text)
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

def clear_canvas():
    global n
    n = None
    canvas.delete("all")  # Clear the canvas
    global recognized_texts, last_x, last_y
    recognized_texts = []  # Clear the recognized texts list
    last_x, last_y = None, None  # Reset drawing coordinates
    label.config(text="")  # Clear the displayed text

# Button to clear the canvas
button_clear = Button(window, text="Clear", command=clear_canvas)
button_clear.grid(row=2, column=1)


# Run the Tkinter event loop
window.mainloop()
