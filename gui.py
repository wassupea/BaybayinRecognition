from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pyautogui    
#from fuzzywuzzy import fuzz
import cv2
import numpy as np   
from recognition import preprocess, segment

def printMessage():

    print("HELLO PO")
class Baybayin_GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.center_window()


        #upper qualifier widget
        self.uqualifier = tk.Canvas(height=60,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.uqualifier.pack()
        self.uqualifier.place(x=97,y=110)
        self.uqualifier.bind("<B1-Motion>",self.udraw)

        #drawing canvas widget
        self.canvas = tk.Canvas(height=170,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.canvas.pack()
        self.canvas.place(x=97,y=170)
        self.canvas.bind("<B1-Motion>",self.draw)

        #bottom qualifier widget
        self.bqualifier = tk.Canvas(height=60,width=700,bg="white",cursor="dotbox",highlightthickness=5)
        self.bqualifier.pack()
        self.bqualifier.place(x=97,y=330)
        self.bqualifier.bind("<B1-Motion>",self.bdraw)


        #title 
        self.lab = tk.Label(text="SINGLE BAYBAYIN RECOGNITION", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                            font=('Lucida Typewriter', 20, ' bold '))
        self.lab.place(x=230, y=20)
        
        #buttons widget
        self.classify_btn = Button(text = 'Classify',state=DISABLED,command=self.get_image,width = 10,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Tahoma',13))
        self.classify_btn.pack()
        self.classify_btn.place(x=230,y=500)

        self.clear_btn = Button(text = "Clear",command=self.clear_canvas,width = 10,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Tahoma',13))
        self.clear_btn.pack()
        self.clear_btn.place(x=390,y=500)


        exit_btn = tk.Button(text = "Close",command=self.close_window,width = 10,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Tahoma',13))
        exit_btn.pack()
        exit_btn.place(x=550,y=500)

    

    def open_window(self):
        new_window=Toplevel(root)
        w = 900
        h = 550
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2) - 20
        y = (hs / 2) - (h / 2) - 50
        new_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
   

        self.lab = tk.Label(new_window,text="BAYBAYIN WORD RECOGNITION", width=28, height=1, fg="#3e7d75",bg="#a1d4cf",
                            font=('Lucida Typewriter', 20, ' bold '))
        self.lab.place(x=120, y=12)
        classify_btn = Button(new_window,text = 'Classify',state=DISABLED,command=printMessage,width = 10,borderwidth=0,bg = '#5899d1',fg = 'white',font = ('Tahoma',13))
        classify_btn.pack()
        classify_btn.place(x=180,y=400)

        clear_btn = Button(new_window,text = "Clear",command=printMessage,width = 10,borderwidth=0,bg ='#4ad977',fg = 'white',font = ('Tahoma',13))
        clear_btn.pack()
        clear_btn.place(x=340,y=400)
        root.resizable(width=False, height=False)

    def printMessage():
        print("HELLO PO")

    # Putting window in center
    def center_window(self):
        w = 900
        h = 550
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
        r =3
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)
    def draw(self, event):
        x , y = event.x,event.y
        r = 3
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)

    def udraw(self, event):
        x , y = event.x,event.y
        r = 3
        self.uqualifier.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)

    def bdraw(self, event):
        x , y = event.x,event.y
        r =3
        self.bqualifier.create_oval(x-r,y-r,x+r,y+r,fill="black")
        self.classify_btn.configure(state=NORMAL)

    def clear_canvas(self):
        self.classify_btn.configure(state=DISABLED)
        self.canvas.delete("all")
        self.bqualifier.delete("all")
        self.uqualifier.delete("all")

    def get_image(self):


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
         #Screen cap the drawing canvas
        upper = './upper.png'
        pyautogui.screenshot(upper, region=(ux, uy, uw, uh))
                #Screen cap the drawing canvas
        lower = './lower.png'
        pyautogui.screenshot(lower, region=(bx, by, bw, bh))

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


