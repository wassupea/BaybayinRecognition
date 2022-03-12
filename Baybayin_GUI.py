from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
from matplotlib.pyplot import title
from recognition import preprocess_segment
import pyautogui    




#RECOGNIZING ALL CHARACTERS AND ACCURATE SO FAR...



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


def close_windows():
    window.destroy()

def clear_canvas():
    canvas.delete("all")


def draw(event):
    x , y = event.x,event.y
    #print(f"X : {x} , Y : {y}")
    r = 5
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="black")
    classify_btn.configure(state=NORMAL)
    
    

def classify_char():
    x, y = canvas.winfo_rootx(), canvas.winfo_rooty()
    w, h = canvas.winfo_width(), canvas.winfo_height()
    written_char = pyautogui.screenshot('./written_chars/sulat.png', region=(x, y, w, h))
    written_char.show()
    baybayin_chars=[]
    digit=preprocess_segment(written_char)
    baybayin_chars.append(digit)
    print('bay: ', baybayin_chars)
    #print(str(digit))
    

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

    exit_btn = tk.Button(text = "Close",command=close_windows,width = 12,borderwidth=0,bg ='#e87d86',fg = 'white',font = ('Lucida Typewriter',16))
    exit_btn.pack()
    exit_btn.place(x=430,y=290)

    canvas.grid(row=0, column=0,padx=30,pady=80)


    canvas.bind("<B1-Motion>",draw)
    tk.mainloop()