from configparser import Interpolation
from tkinter import *
import tkinter as tk
from tkinter.tix import IMAGE
from turtle import right
from PIL import ImageGrab , ImageTk ,Image
from cv2 import resize
import pyscreenshot
import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
from keras.models import load_model

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
    written_char = ImageGrab.grab(bbox=(400,215,780,530))
    written_char.save('./written_chars/sulat.png','PNG')
    baybayin_chars = []
    digit=preprocess_segment(written_char)
    baybayin_chars.append(digit)
    #written_char.show()
    #print(str(digit))

    

    for baybayin_char in baybayin_chars:
        if baybayin_char==0:
            output ='a'
        elif baybayin_char==1:
            output ='ba'
        elif baybayin_char==2:
            output = 'da/ra'
        elif baybayin_char==3:
            output = 'e/i'
        elif baybayin_char==4:
            output == 'ga'
        elif baybayin_char==5:
            output ='ha'
        elif baybayin_char==6:
            output ='ka'
        elif baybayin_char==7:
            output ='kuw'
        elif baybayin_char==8:
            output ='la'
        elif baybayin_char==9:
            output ='ma'
        elif baybayin_char==10:
            output ='na'
        elif baybayin_char==11:
            output ='nga'
        elif baybayin_char==12:
            output ='o/u'
        elif baybayin_char==13:
            output ='pa'
        elif baybayin_char==14:
            output='sa'
        elif baybayin_char==15:
            output='ta' 
        elif baybayin_char==16:
            output='tul'
        elif baybayin_char==17:
            output='wa' 
        elif baybayin_char==18:
            output='ya' 

    print(output)
    
    
#function for image preprocess and image segmentation

def preprocess_segment():
    count=1


    #x= canvas.winfo_rootx()+canvas.winfo_rootx()
    #y= canvas.winfo_rooty()+canvas.winfo_rooty()
    #x1=x+canvas.winfo_width()
    #y1=y+canvas.winfo_height()

    image_name = "written_chars" + str(count+1) +".png"

    written_char = ImageGrab.grab(bbox=(400,215,780,530))

    #ImageGrab.grab().crop((x,y,x1,y1)).save(image_name)
    
    written_char.save(image_name)
    
    baybayin_chars = []
    segmented = []
    


    image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

    #create a binary threshold image

    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_BINARY)


    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # draw all contours
    with_contours = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)

    
   
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(with_contours,(x,y), (x+w,y+h), (0,255,0), 1)
        cropped_contour= binary[y:y+h, x:x+w]
        
        resize_contour = cv2.resize(cropped_contour, (64, 64), interpolation=cv2.INTER_AREA)
        img_reshape = resize_contour.reshape(1,64,64,1)
        image_reshape = img_reshape / 255.0

        pred = model.predict([image_reshape])
        final = np.argmax(pred)
        print(final)
        
        cv2.imshow('Image',cropped_contour)
        cv2.waitKey(0)
        #resize_contour = cv2.resize(cropped_contour, (64, 64), interpolation=cv2.INTER_AREA)

        #if (resize_contour.shape) == 3:
            #resize_contour = cv2.cvtColor(resize_contour, cv2.COLOR_BGR2GRAY)

        #print(len(resize_contour))
        #print(resize_contour.shape)
        #img_reshape = resize_contour.reshape(1,64,64,1)
        #image_reshape = img_reshape / 255.0
        #img_name = "written_chars" + str(count+1) +".png"
        #cv2.imwrite(img_name,resize_contour)
        #cv2.imread(img_name)
        #cv2.imshow('Image',resize_contour)
        #cv2.waitKey(0)
        #segmented.append(image_reshape)
        #print(len(segmented))
        #print('Segmented shape:', np.array(segmented).shape)

        #predict = model.predict([segmented])[0]
        #final_predict = np.argmax(predict)
        #print(final_predict)

        #return final_predict


if __name__ == '__main__':
    window = tk.Tk() # create a Tk root window
    window.configure(background='#a1d4cf')
    window.title("Baybayin Character Recognition")
    center_window()

    canvas = tk.Canvas(height=300,width=366,bg="white",cursor="dotbox",highlightthickness=5)
    lab = tk.Label(window, text="WRITE BAYBAYIN CHARACTERS", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                        font=('Lucida Typewriter', 20, ' bold '))
    lab.place(x=60, y=12)

    classify_btn = tk.Button( text = 'Classify',state=DISABLED,command=preprocess_segment,width = 12,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Lucida Typewriter',16))
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