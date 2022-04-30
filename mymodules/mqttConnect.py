
import time
import paho.mqtt.client as paho
from paho import mqtt
from mymodules import Driver

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic=="driver/register/1010/getFP":
       print(msg.payload.decode())
       Driver.getDriverFingerPrint(msg.payload.decode())
    elif msg.topic == "/testback":
      print("we are testing")
    elif msg.topic == "registration":
      print("checking the driver reg status")
      print(msg.payload.decode())
      if msg.payload.decode()=="done":
          print("indicate on the db that we were successful")
      else:
          print("dont indicate on the db that we were successful")
    else:
      print("unknown topic")
    #Driver.getDriverFingerPrint()
def on_disconnect(client, userdata, rc):
    print("Disconnected" % rc)
def connectMqtt():
    
    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    global client 
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set("Francois", "12345Fra")
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("9c641868feef4f288cb222c3d38b905e.s1.eu.hivemq.cloud", 8883)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    client.subscribe("/testback", qos=1)
    client.subscribe("driver/register/1010/getFP", qos=1)
    client.subscribe("registration", qos=1)

    # a single publish, this can also be done in loops, etc.


    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_start()

def driverMqtt(topic,data):
    client.publish(topic, payload=data, qos=1)
