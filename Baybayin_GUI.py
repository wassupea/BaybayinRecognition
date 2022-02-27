from tkinter import *
import tkinter as tk
from PIL import ImageGrab , ImageTk ,Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model


# Load Model
model = load_model('./baybayin_model1.h5')

def draw(event):
    x , y = event.x,event.y
    #print(f"X : {x} , Y : {y}")
    r = 8
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
    classify_btn.configure(state=NORMAL)


# Function for exit.
def close_canvas():
    window.destroy()

# Fucntion clearing canvas.
def clear_canvas():
    canvas.delete("all")



#Function for capturing the written character
def classify_char():
    written_char = ImageGrab.grab(bbox=(400,215,780,530))
    written_char.save('./written_chars/sulat.png','PNG')
    digit=recognize_char(written_char)
    written_char.show()
    print(str(digit))

    lab1 = tk.Label(window, text='Predicted Digit is : ' + output, width=24, height=2, fg="#3e7d75", bg="black",
                   font=('Lucida Typewriter', 16, ' bold '))
    lab1.place(x=10, y=420)

    for digits in digit:
        if digits==0:
            output+='a'
        elif digits==1:
            output+='ba'
        elif digits==2:
            output+='da/ra'
        elif digits==3:
            output+='e/i'
        elif digits==4:
            output+='ga'
        elif digits==5:
            output+='ha'
        elif digits==6:
            output+='ka'
        elif digits==7:
            output+='kuw'
        elif digits==8:
            output+='la'
        elif digits==9:
            output+='ma'
        elif digits==10:
            output+='na'
        elif digits==11:
            output+='nga'
        elif digits==12:
            output+='o/u'
        elif digits==13:
            output+='pa'
        elif digits==14:
            output+='sa'
        elif digits==15:
            output+='ta' 
        elif digits==16:
            output+='tul'
        elif digits==17:
            output+='wa' # or i
        elif digits==18:
            output+='ya' # or u
    return output

    
        
#Function for preprocessing the image then passing it to the model for the prediction.
def recognize_char(image):
    char_image = cv2.imread('./written_chars/sulat.png')
    grey = cv2.cvtColor(char_image.copy(), cv2.COLOR_BGR2GRAY)
    returns, thresh = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    contours, hierachy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    preprocessed_digits = []
    filtered_image = cv2.resize(char_image,(64,64))
    if len(filtered_image.shape) == 3:
        filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
    
    res = model.predict(filtered_image.reshape(1, 64, 64, 1))
    return np.argmax(res)


def center_window():
    # Putting window in center
    w = 600
    h = 450

    ws = window.winfo_screenwidth() #1366
    hs = window.winfo_screenheight() #768
    #print(ws,hs)
    x = (ws / 2) - (w / 2) - 20
    y = (hs / 2) - (h / 2) - 50
    #print(x,y)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.resizable(width=False, height=False)




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
