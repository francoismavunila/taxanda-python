import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)

def doorlock(comm):
	if comm=="lock":
		GPIO.output(26,GPIO.LOW)
		GPIO.output(19,GPIO.HIGH)
	elif comm=="open":
		GPIO.output(19,GPIO.LOW)
		GPIO.output(26,GPIO.HIGH)
		
