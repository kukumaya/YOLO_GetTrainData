import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import math
import datetime
sys.setrecursionlimit(10000)

shiftclicked = False 
step = 1
opttime = datetime.datetime.now()
boxtext = ''
imagename = ''
formatsize = 416
def selectimage():
    filepath = askopenfilename(filetypes = (("Image files", "*.jpg;*.png")
                                                        ,("All files", "*.*") ))
    if(filepath is None or filepath==''):
        return
    global imagename
    imagename=filepath.split('/')[-1]
    
    global image
    image = Image.open(filepath) 
                                                          
    w, h = image.size 
    global formatsize
    size = w if w > h else h
    if(size > formatsize):
        Resize(size / formatsize)
    canvas.delete("all")
    img = ImageTk.PhotoImage(image)  
    canvas.create_image(0,0 ,anchor="nw",image=img)  
    createrect(20, 20, 20 + w/2, 20 + h/2)
    
def Resize(sizerate):
    global image
    global imagename
    w, h = image.size 
    wnew,hnew=math.trunc(w / sizerate),math.trunc(h / sizerate)
    print(wnew,hnew)
    image.thumbnail((wnew,hnew), Image.ANTIALIAS)
    image.save(imagename)
    pass    
def createrect(_x0,_y0,_x1,_y1):
    global x0
    global y0
    global x1
    global y1
    global rect  
    x0 = _x0
    x1 = _x1
    y0 = _y0
    y1 = _y1  
    rect = canvas.create_rectangle(x0, y0, x1, y1)    
    mainwindow.mainloop()

def adjustrect(_x = 0, _y = 0, _w = 0, _h = 0):
    global x0
    global y0
    global x1
    global y1
    global rect
    try:
        canvas.delete(rect) 
    except NameError:
        tk.messagebox.showwarning("NoImage","Select Image First!")
        return
    
    x0 += _x
    x1 += _x
    
    y0 += _y
    y1 += _y

    x0 -= _w/2
    x1 += _w/2
    
    y0 -= _h/2
    y1 += _h/2

    rect = canvas.create_rectangle(x0, y0, x1, y1)    
    mainwindow.mainloop()
def AutoStep():
    global step
    global opttime
    if((datetime.datetime.now() - opttime).total_seconds()<0.5):
        step *= 2
    else:
        step = 1 
    opttime = datetime.datetime.now()

def left():
    AutoStep()
    adjustrect(_x=-step)
def right():
    AutoStep()
    adjustrect(_x=step)     
def up():
    AutoStep()
    adjustrect(_y=-step)
def down():
    AutoStep()
    adjustrect(_y=step)
def increasewidth():
    AutoStep()
    adjustrect(_w=step)
def decreasewidth():
    AutoStep()
    adjustrect(_w=-step)
def increaseheight():
    AutoStep()
    adjustrect(_h=step)
def decreaseheight():
    AutoStep()
    adjustrect(_h=-step) 
def SaveBox():
    if(classinput.get()==''):
        tk.messagebox.showwarning("NoClass","Please Enter ClassCode First")
        return
    global boxtext
    global x0
    global y0
    global x1
    global y1
    boxtext +=" {0} {1} {2} {3} {4}".format(x0, y0, x1, y1,classinput.get())

def SaveRow():
    global imagename
    global boxtext
    if(boxtext==''):
        tk.messagebox.showwarning("NoBox","Please Save Box First")
        return
    CreateTrainTxt(imagename + boxtext)
    boxtext = "" 

def EventCheck():
    pass
def DoNothing():
    pass 
def CreateTrainTxt(text):
    file= open("train.txt","w+")
    file.write(text)
    file.close()

mainwindow = tk.Tk()
mainwindow.title('GetTrainData')
mainwindow.geometry("800x600") #You want the size of the app to be 500x500
keyEvents= {"Left"      : lambda x:left(),
    "Right"      : lambda x:right(),
    "Up"         : lambda x:up(),
    "Down"       : lambda x:down(),
    "Control-Left"  : lambda x:decreasewidth(),
    "Control-Right" : lambda x:increasewidth(),
    "Control-Up"    : lambda x:increaseheight(),
    "Control-Down"  : lambda x:decreaseheight(),
    "Control-f"     :lambda x:selectimage(),
    "Control-q"     :lambda x:mainwindow.quit(),
    "Control-n"     :lambda x:SaveBox(),
    "Control-s"     :lambda x:SaveRow()
    }

for key,value in keyEvents.items():
    mainwindow.bind("<{0}>".format(key),value)
 
############ The First row
canvas = tk.Canvas(mainwindow, width =426, height=426)  
canvas.grid(row=0, column=1, columnspan=4) 
 
mainwindow.grid_columnconfigure((0, 5), weight=1) 
 
################# The Second row
tk.Label(mainwindow,text="Please Enter the ClassCode", fg = "red", font = "Helvetica 12 bold").grid(row = 1,column =1,columnspan=2,sticky="e")
classinput = tk.Entry(mainwindow, font = "Helvetica 12 bold") 
classinput.grid(row =1 ,column =3, columnspan = 2, sticky= "w")
################# The Third row & Fourth row
frmbuttons= {
    "SelectImage(ctrl-f)"      : selectimage,
    "SaveBox(ctrl-n)"      : SaveBox,
    "SaveRow(ctrl-s)"      : SaveRow,
    "Close(ctrl-q)"      : quit,
    "MoveLeft(←)"      : left,
    "MoveRight(←)"      : right,
    "MoveUp(↑)"         : up,
    "MoveDown(↓)"       : down,    
    "IncreaseWidth(shift-→)" : increasewidth,
    "IncreaseHeight(shift-↑)"    : increaseheight,
    "DecreaseWidth(shift+←)"  : decreasewidth,
    "DecreaseHeight(shift+↓)"  : decreaseheight 
    }

global colindex
colindex=0
for key,value in frmbuttons.items():
    colindex += 1
    btn = tk.Button(mainwindow, 
                text=key, 
                fg="red",
                command=value)
    btn.grid(row=math.trunc((colindex-1)/4)+2, column=(colindex-1)%4+1) 
 
mainwindow.mainloop() 
    