from tkinter import *
import tkinter as tk
from PIL import ImageGrab
import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model



## SEGMENTED - ALL WRITTEN CHARACTERS ARE RECOGNIZED BUT NOT ACCURATE


model = load_model('./baybayin_model1.h5') 

def draw(event):
    x , y = event.x,event.y
    r = 6
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
    classify_btn.configure(state=NORMAL)
    

# Function for exit.
def close_canvas():
    window.destroy()

# Fucntion clearing canvas.
def clear_canvas():
    canvas.delete("all")


        

def center_window():
    # Putting window in center
    w = 600
    h = 450

    ws = window.winfo_screenwidth() #1366
    hs = window.winfo_screenheight() #768
    x = (ws / 2) - (w / 2) - 20
    y = (hs / 2) - (h / 2) - 50
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.resizable(width=False, height=False)


def classify_char():
    print ('-------RUNNING BAYBAYIN_RECOGNITION_SYSTEM.py -------')
    written_char = ImageGrab.grab(bbox=(400,215,780,530))
    written_char.save('./written_chars/sulat.png','PNG')
    baybayin_chars = []

    image = cv2.imread('./written_chars/sulat.png')
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

  
    returns, binary = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    contours, hierachy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    image_copy=image.copy()
    

    preprocessed=[]

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        # Creating a rectangle around the digit in the original image (for displaying the digits fetched via contours)
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

       
        chars = binary[y:y + h, x:x + w]


        resized_chars = cv2.resize(chars, (64, 64))
        

        img_reshape = resized_chars.reshape(1,64,64,1)
        img_reshape = img_reshape / 255
        
        pred = model.predict([img_reshape])[0]
        final = np.argmax(pred)
        print(final)      
        cv2.imshow('im', resized_chars)
        cv2.waitKey(0)

    
    
    

if __name__ == '__main__':
    window = tk.Tk() # create a Tk root window
    window.configure(background='#a1d4cf')
    window.title("Baybayin Character Recognition")
    center_window()

    canvas = tk.Canvas(height=300,width=366,bg="white",cursor="dotbox",highlightthickness=5)
    lab = tk.Label(window, text="WRITE BAYBAYIN CHARACTERS", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                        font=('Lucida Typewriter', 20, ' bold '))
    lab.place(x=60, y=12)

    classify_btn = tk.Button( text = 'Classify',state=DISABLED,command=classify_char,width = 12,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Lucida Typewriter',16))
    classify_btn.pack()
    classify_btn.place(x=430,y=150)

    clear_btn = tk.Button(text = "Clear Window",command=clear_canvas,width = 12,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Lucida Typewriter',16))
    clear_btn.pack()
    clear_btn.place(x=430,y=220)

    exit_btn = tk.Button(text = "Close",command=close_canvas,width = 12,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Lucida Typewriter',16))
    exit_btn.pack()
    exit_btn.place(x=430,y=290)

    # setting elements on particular position on screen.
    canvas.grid(row=0, column=0,padx=30,pady=80)

    # Event occurs while dragging mouse
    canvas.bind("<B1-Motion>",draw)
    tk.mainloop()