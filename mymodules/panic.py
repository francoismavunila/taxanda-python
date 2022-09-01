from mymodules import gps
import time
import datetime
import json
from mymodules import mqttConnect

def panic():
	while True:
		currentDT = datetime.datetime.now()
		panicData={
			"device_id":1010,
			"time": currentDT.strftime("%m/%d/%Y, %H:%M:%S"),
			"latitude": gps.getCoordinates()['latitude'],
			"longitude":gps.getCoordinates()['longitude']
		}
		my_json_object = json.dumps(panicData)
		print(my_json_object)
		mqttConnect.driverMqtt("activity/1010/panic",my_json_object)
		time.sleep(2)
