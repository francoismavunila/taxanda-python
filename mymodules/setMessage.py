import tkinter as tk
def setFrame(frame):
    global frm
    frm=frame
    global display
    global var
    var = tk.StringVar()
    display = tk.Message( frm,textvariable=var,font = "120",width=500)
    display.pack()
def setMess(mess):
    print(mess)
    print(var)
    var.set(mess)
    
