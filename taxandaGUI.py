import tkinter as tk

window = tk.Tk()
frame = tk.Frame(window)
frame.pack()

bottomframe = tk.Frame(window)
bottomframe.pack( side = tk.BOTTOM )


def ride():
  var.set("ride pressed")
def arrival():
  var.set("arrival pressed")
def panic():
  var.set("driver panic")
window.geometry('850x580') 
var = tk.StringVar()
display = tk.Message( frame, textvariable=var,font = "250",fg="white",bg="Navyblue",width=500,pady=10)
Ride =  tk.Button(bottomframe, text="Ride",command=ride,activebackground="blue",bg="green",height=10,width=30)
Arrival =  tk.Button(bottomframe, text="Arrival",command=arrival,activebackground="blue",bg="green",height=10,width=30)
Panic = tk.Button(bottomframe, text="Panic",command=panic,activebackground="blue",bg="red",height=10,width=30)

display.pack(side=tk.TOP)
var.set("Welcome to Our safe taxis")
Ride.pack(side=tk.RIGHT)
Arrival.pack(side=tk.LEFT)
Panic.pack()
window.mainloop()

