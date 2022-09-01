import tkinter as tk
from mymodules import mqttConnect
from mymodules import setMessage
from mymodules import ride
from mymodules import Driver
from mymodules import Passenger
from mymodules import doorlock
from mymodules import panic
import threading

doorlock.doorlock("lock")
def test():
    print("working")
    setMessage.setMess("hgfd")
window = tk.Tk()
frame = tk.Frame(window)
frame.pack()

bottomframe = tk.Frame(window)
bottomframe.pack( side = tk.BOTTOM )
setMessage.setFrame(frame)


window.geometry('850x580')
window.config(bg='#222222')


Ride =  tk.Button(bottomframe, text="Ride",command=lambda:threading.Thread(target=ride.rideAuth).start(),activebackground="blue",bg="green",height=10,width=30)
Arrival =  tk.Button(bottomframe, text="Arrival",command=lambda:threading.Thread(target=ride.arrivalAuth).start(),activebackground="blue",bg="green",height=10,width=30)
Panic = tk.Button(bottomframe, text="Panic",command=lambda:threading.Thread(target=panic.panic).start(),activebackground="blue",bg="red",height=10,width=30)


Ride.pack(side=tk.RIGHT)
Arrival.pack(side=tk.LEFT)
Panic.pack()

#threading.Thread(target=mqttConnect.connectMqtt())
mqttConnect.connectMqtt()
window.mainloop()

