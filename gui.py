from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pyautogui    
import cv2
import numpy as np   
from preprocess_segmentation import preprocess, segment
from recognition import recognize
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
import time
from PIL import Image




def printMessage():

    print("HELLO PO")
class Baybayin_GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.center_window()
        self.eraser_on = False

        eraser_image = PhotoImage(file='eraser-icon-6.png')
        pen_image = PhotoImage(file='pen.png')
        pen_image = pen_image.subsample(4,4)
        eraser_image = eraser_image.subsample(4,4)

        #upper qualifier widget
        self.uqualifier = tk.Canvas(height=60,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.uqualifier.pack()
        self.uqualifier.place(x=97,y=106)
        self.uqualifier.bind("<B1-Motion>",self.udraw)

        #drawing canvas widget
        self.canvas = tk.Canvas(height=170,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.canvas.pack()
        self.canvas.place(x=97,y=170)
        self.canvas.bind("<B1-Motion>",self.draw)

        #bottom qualifier widget
        self.bqualifier = tk.Canvas(height=60,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.bqualifier.pack()
        self.bqualifier.place(x=97,y=350)
        self.bqualifier.bind("<B1-Motion>",self.bdraw)


        #title 
        self.lab = tk.Label(text="WRITE BAYBAYIN CHARACTERS", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                            font=('Lucida Typewriter', 20, ' bold '))
        self.lab.place(x=122, y=25)

        #buttons of the interface
        self.instructions_btn = Button(text = "Instructions",command=self.open_reminder,width = 10,borderwidth=0,bg = '#d59bf6', fg = 'white',font = ('Tahoma',13))
        self.instructions_btn.pack()
        self.instructions_btn.place(x=55,y=530)

        self.chart_btn = Button(text = "Chart",command=self.open_chart,width = 10,borderwidth=0,bg = '#ead865',fg = 'white',font = ('Tahoma',13))
        self.chart_btn.pack()
        self.chart_btn.place(x=210,y=530)
        
        self.classify_btn = Button(text = 'Classify',state=DISABLED,command=self.get_image,width = 10,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Tahoma',13))
        self.classify_btn.pack()
        self.classify_btn.place(x=370,y=530)
        
        self.eraser_btn = Button(image = eraser_image,command=self.use_eraser,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Tahoma',13))
        self.eraser_btn.image = eraser_image
        self.eraser_btn.pack()
        
        self.eraser_btn.place(x=840,y=180)

        self.pen_btn = Button(text='P',image = pen_image,command=self.use_pen)
        self.pen_btn.image = pen_image
        self.pen_btn.place(x=840,y=255)


        self.clear_btn = Button(text = "Clear",command=self.clear_canvas,width = 10,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Tahoma',13))
        self.clear_btn.pack()
        self.clear_btn.place(x=530,y=530)

        exit_btn = tk.Button(text = "Close",command=self.close_window,width = 10,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Tahoma',13))
        exit_btn.pack()
        exit_btn.place(x=690,y=530)



    # Putting window in center
    def center_window(self):
        w = 900
        h = 620
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2) - 20
        y = (hs / 2) - (h / 2) - 50
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.resizable(width=False, height=False)


    def open_reminder(self):
        remindersimg = cv2.imread('reminders.png')
        
        cv2.imshow('Reminders',remindersimg)

    def open_chart(self):
        chartimg = cv2.imread('chart.png')
        
        cv2.imshow('Chart',chartimg)

    def close_window(self):
        root.destroy()

    #function to draw on the middle part
    def draw(self, event):
        
        x , y = event.x,event.y

        #changing the paint color to white if eraser is activated
        if self.eraser_on:
            r = 15
            self.canvas.create_line(x-r,y-r,x+r,y+r,fill="white")
            
        #if draw is activated the paint color will change to black
        else:
            r = 3
            self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
            
        self.classify_btn.configure(state=NORMAL)

    #function to draw on the upper part
    def udraw(self, event):
        x , y = event.x,event.y
        if self.eraser_on:
            r = 10
            self.uqualifier.create_line(x-r,y-r,x+r,y+r,fill="white")
        else:
            r = 3
            self.uqualifier.create_oval(x-r,y-r,x+r,y+r,fill="black")
            
        self.classify_btn.configure(state=NORMAL)

    #function to draw on the bottom part
    def bdraw(self, event):
        x , y = event.x,event.y
        if self.eraser_on:
            r = 10
            self.bqualifier.create_line(x-r,y-r,x+r,y+r,fill="white")
        else:
            r = 3
            self.bqualifier.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)

    #function to clear canvas
    def clear_canvas(self):
        self.classify_btn.configure(state=DISABLED)
        self.eraser_on = False
        self.canvas.delete("all")
        self.bqualifier.delete("all")
        self.uqualifier.delete("all")

        #destroying labels of output
        try:
            lab1.destroy()
            lab2.destroy()
        except:
            pass

    #activating eraser
    def use_eraser(self):
        self.eraser_on = True

    #activating drawing mode
    def use_pen(self):
        self.eraser_on = False        

    #screen capturing of the drawing canvas
    def get_image(self):
        self.eraser_on = False

        #getting the x,y, w, h coordinates of the drawing canvas
        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        ux, uy = self.uqualifier.winfo_rootx(), self.uqualifier.winfo_rooty()
        uw, uh = self.uqualifier.winfo_width(), self.uqualifier.winfo_height()

        bx, by = self.bqualifier.winfo_rootx(), self.bqualifier.winfo_rooty()
        bw, bh = self.bqualifier.winfo_width(), self.bqualifier.winfo_height()
        

        #Screen cap the drawing canvas
        path = './sulat.png'
        pyautogui.screenshot(path, region=(x, y, w, h))
        upper = './upper.png'
        pyautogui.screenshot(upper, region=(ux, uy, uw, uh))
        lower = './lower.png'
        pyautogui.screenshot(lower, region=(bx, by, bw, bh))

        #read the image
        image = cv2.imread(path)

        #changing the image color to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #converting saved screen cap to numpy array
        array_image = np.array(image)

        hello = self.classify_image(array_image) #Passing the image for the classification process
        return hello


    def classify_image(self,img):
    #Steps for Classification of Characters
            #1 Image Preprocessing
            #2 Image Segmentation
            #3 Feature Extraction   (Held by the imported cnn model)
            #4 Classification       (Held by the imported cnn model)

        #clearing label output
        global lab1,lab2
        try:
            lab1.destroy()
            lab2.destroy()
        except:
            pass
        baybayin_chars=""

        
        preprocessed_image = preprocess(img)  #Preprocessing image or Image enhancement
        start = time.time()
        segment_image = segment(img)
        messagebox.showinfo(title='Classifying...', message='Please wait for a few seconds')

        #activating timer
        

        recognize_image = recognize(segment_image)
        try:
            baybayin_chars+= "'"+ recognize_image + "'"
        except:
            baybayin_chars+="no translation"
            
        end = time.time()
         
        process_time = end - start
        
        float_time = float("{:.2f}".format(process_time))
        float_time= str(float_time)
        display_time = 'Time: '+float_time+"s"

        #Label for output and time
        lab1 = Label(root, text=baybayin_chars, width=40, height=2, fg="white", bg="#a1d4cf",
                   font = ('Tahoma',11))
        lab1.place(x=255, y=430)
        lab2 = Label(root, text=display_time, width=10, height=2, fg="white", bg="#a1d4cf",
                   font = ('Tahoma',10))
        lab2.place(x=25, y=430)
        return baybayin_chars



if __name__ == '__main__':

    root = Tk()
    root.configure(background='#a1d4cf')
    root.title("Baybayin Character Recognition")

    b = Baybayin_GUI(root)
    root.mainloop()
    


    
