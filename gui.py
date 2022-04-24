from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pyautogui    
#from fuzzywuzzy import fuzz
import cv2
import numpy as np   
from recognition import preprocess, segment
class Baybayin_GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.center_window()

        #drawing canvas widget
        self.canvas = tk.Canvas(height=200,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.canvas.pack()
        self.canvas.place(x=47,y=80)
        self.canvas.bind("<B1-Motion>",self.draw)


        #title 
        self.lab = tk.Label(text="WRITE BAYBAYIN CHARACTERS", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                            font=('Lucida Typewriter', 20, ' bold '))
        self.lab.place(x=120, y=12)
        
        #buttons widget
        self.classify_btn = Button(text = 'Classify',state=DISABLED,command=self.get_image,width = 10,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Tahoma',13))
        self.classify_btn.pack()
        self.classify_btn.place(x=180,y=400)

        self.clear_btn = Button(text = "Clear",command=self.clear_canvas,width = 10,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Tahoma',13))
        self.clear_btn.pack()
        self.clear_btn.place(x=340,y=400)

        exit_btn = tk.Button(text = "Close",command=self.close_window,width = 10,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Tahoma',13))
        exit_btn.pack()
        exit_btn.place(x=500,y=400)

    

    
    def printMessage(self):
        print("HELLO PO")

    # Putting window in center
    def center_window(self):
        w = 800
        h = 450
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2) - 20
        y = (hs / 2) - (h / 2) - 50
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.resizable(width=False, height=False)

    def close_window(self):
        root.destroy()

    def draw(self, event):
        x , y = event.x,event.y
        r = 5
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)

    def clear_canvas(self):
        self.classify_btn.configure(state=DISABLED)
        self.canvas.delete("all")

    def get_image(self):


        #getting the x,y, w, h coordinates of the drawing canvas
        x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        

        #Screen cap the drawing canvas
        path = './sulat.png'
        pyautogui.screenshot(path, region=(x, y, w, h))

        #path.show()
        image = cv2.imread(path)
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

        baybayin_chars=[]
        preprocessed_image = preprocess(img)  #Preprocessing image or Image enhancement
        segment_image = segment(img)
        #recognize_image = recognition(segment_image)
        baybayin_chars.append(segment_image)
        
        messagebox.showinfo(title='Written Baybayin Characters', message=baybayin_chars)
        
        return baybayin_chars
    



if __name__ == '__main__':

    root = Tk()
    root.configure(background='#a1d4cf')
    root.title("Baybayin Character Recognition")

    b = Baybayin_GUI(root)
    root.mainloop()


