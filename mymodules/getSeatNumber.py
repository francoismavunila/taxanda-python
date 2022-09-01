import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) 
GPIO.setup(24, GPIO.IN) 
GPIO.setup(17, GPIO.IN) 
GPIO.setup(22, GPIO.IN) 
GPIO.setup(27, GPIO.IN) 
def getDriverSeat():
    driverSeat=GPIO.input(23)
    print(driverSeat)
    return driverSeat
def getSeatNumber():
    passSeats=0
    seat1 = GPIO.input(24)
    if(seat1):
        passSeats=passSeats+1
        print("24")

    seat2 = GPIO.input(17)
    if(seat2):
        passSeats=passSeats+1
        print("17")

    seat3 = GPIO.input(22)
    if(seat3):
        passSeats=passSeats+1
        print("22")

    seat4 = GPIO.input(27)
    if(seat4):
        passSeats=passSeats+1
        print("27")
    #print(passSeats)
    return passSeats
    
#while(1):
    #time.sleep(2)
    #print('*******')
    #getSeatNumber()
    #print('########')
