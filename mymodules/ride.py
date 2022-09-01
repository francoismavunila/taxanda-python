from mymodules import setMessage
from mymodules import Driver
from mymodules import Passenger
def rideAuth():
    #get driver's fp
    id=Driver.getDriverFingerPrint()
    if(id==0):
        #get pass fp
        setMessage.setMess("done on driver's side, enrolling passenger now")
        Passenger.enrollPaasengerFingerPrint()
    else:
        #failed to get driver fp
        #setMessage.setMess("failed to authenticate driver")
        return False
def arrivalAuth():
    #get driver's fp
    id=Driver.getDriverFingerPrint()
    if(id==0):
        #get pass fp
        setMessage.setMess("done on driver's side, enrolling passenger now")
        Passenger.passengerArrival()
    else:
        #failed to get driver fp
        #setMessage.setMess("failed to authenticate driver")
        return False
     
