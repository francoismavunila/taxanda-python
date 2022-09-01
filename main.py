from mymodules import Driver
from mymodules import mqttConnect
from mymodules import Passenger

while True:
    print("----------------")
    print("a) register driver")
    print("b) send")
    print("d) delete driver fingerprint")
    print("da) clear driver database")
    print("dp) clear passenger database")
  
    z = input("> ")

    if z == "a":
        Passenger.getTemplate()
    if z == "d":
        Driver.delete_fingerprint()
    if z == "da":
        Driver.clearDriverInfo()
    if z == "dp":
        Passenger.clearDriverInfo()
  
