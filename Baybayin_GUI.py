from tkinter import *
import tkinter as tk
from PIL import ImageGrab , ImageTk ,Image
import pyscreenshot

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

def classify_char():
    #
    #im = ImageGrab.grab(bbox=(321,130,1300,510))
    #im.save('./written_chars/sulat.png','PNG')
    #im = ImageGrab.grab(bbox=(321,130,1000,510))
    #im.save('./written_chars/sulat2.png','PNG')
    #im = ImageGrab.grab(bbox=(350,130,1000,510))
    #im.save('./written_chars/sulat3.png','PNG')
    #im = ImageGrab.grab(bbox=(350,200,1000,10))
    #im.save('./written_chars/sulat4.png','PNG')
    im = ImageGrab.grab(bbox=(351,200,1000,550))
    im.save('./written_chars/sulat5.png','PNG')

def center_window():
    # Putting window in center
    w = 600
    h = 450

    ws = window.winfo_screenwidth() #1366
    hs = window.winfo_screenheight() #768
    print(ws,hs)
    x = (ws / 2) - (w / 2) - 20
    y = (hs / 2) - (h / 2) - 50
    print(x,y)
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
