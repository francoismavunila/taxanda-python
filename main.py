from mymodules import Driver
from mymodules import mqttConnect
mqttConnect.connectMqtt()

while True:
    print("----------------")
    print("a) register driver")
    print("b) send")
    print("d) delete driver fingerprint")
  
    z = input("> ")

    if z == "a":
        Driver.getDriverFingerPrint("28-156159v28")
    if z == "d":
        Driver.delete_fingerprint()
    if z == "b":
        mqttConnect.driverMqtt("testing")
  
