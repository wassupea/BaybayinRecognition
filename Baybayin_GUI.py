# Importing of important modules.
from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
from recognition import preprocess, recognition, segment
import cv2
import pyautogui    
import numpy as np




#RECOGNIZING ALL CHARACTERS AND ACCURATE SO FAR...



#For positioning the system at the center
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


#Close function of the system
def close_windows():
    window.destroy()


#Function for clearing the drawing canvas
def clear_canvas():
    canvas.delete("all")


#Function for writing on the canvas
def draw(event):
    x , y = event.x,event.y
    r = 5
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
    classify_btn.configure(state=NORMAL)
    


#Function for capturing the written characters as an image
def get_image():

    #getting the x,y, w, h coordinates of the drawing canvas
    x, y = canvas.winfo_rootx(), canvas.winfo_rooty()
    w, h = canvas.winfo_width(), canvas.winfo_height()
    
    #Screen cap the drawing canvas
    path = './written_chars/sulat.png'
    pyautogui.screenshot(path, region=(x, y, w, h))
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #converting saved screen cap to numpy array
    array_image = np.array(image)

    hello = classify_image(array_image) #Passing the image for the classification process
    return hello

    
#Function for Recognition/Classification of the Written Characters
def classify_image(img):

    #Steps for Classification of Characters
            #1 Image Preprocessing
            #2 Image Segmentation
            #3 Feature Extraction   (Held by the imported cnn model)
            #4 Classification       (Held by the imported cnn model)

    baybayin_chars=[]
    preprocessed_image = preprocess(img)  #Preprocessing image or Image enhancement
    segment_image = segment(img)
    #recognize_image = recognition(segment_image)
    baybayin_chars.append(segment_image)
    tk.messagebox.showinfo(title='Written Baybayin Characters', message=baybayin_chars)
     
    return baybayin_chars



if __name__ == '__main__':

    #GUI BUILD
    window = tk.Tk() # create a Tk root window
    window.configure(background='#a1d4cf')
    window.title("Baybayin Character Recognition")
    center_window()

    canvas = tk.Canvas(height=300,width=366,bg="white",cursor="dotbox",highlightthickness=5)
    lab = tk.Label(window, text="WRITE BAYBAYIN CHARACTERS", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                        font=('Lucida Typewriter', 20, ' bold '))
    lab.place(x=60, y=12)

    classify_btn = tk.Button( text = 'Classify',state=DISABLED,command=get_image,width = 12,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Lucida Typewriter',16))
    classify_btn.pack()
    classify_btn.place(x=430,y=150)

    clear_btn = tk.Button(text = "Clear Window",command=clear_canvas,width = 12,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Lucida Typewriter',16))
    clear_btn.pack()
    clear_btn.place(x=430,y=220)

    exit_btn = tk.Button(text = "Close",command=close_windows,width = 12,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Lucida Typewriter',16))
    exit_btn.pack()
    exit_btn.place(x=430,y=290)

    canvas.grid(row=0, column=0,padx=30,pady=80)


    canvas.bind("<B1-Motion>",draw)
    tk.mainloop()