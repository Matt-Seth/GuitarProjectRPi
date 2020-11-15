#EE 250 Project

import paho.mqtt.client as mqtt
import time
import sys
import MicToFTransform as mic
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi', by giving the path below
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

from grovepi import*
from grove_rgb_lcd import*

led = 3

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    
    # When the client receives a CONNACK message from the broker in response to the
    # connect it generates an on_connect() callback.
    client.on_connect = on_connect
    
    client.connect(host="ec2-3-138-142-104.us-east-2.compute.amazonaws.com", port=60000, keepalive=60)
    client.loop_start()
    stream = mic.mic_init()

    while True:
        #Sensor Readings
        try:
            note = ""
            note = mic.getNote(stream)
            print(note)
            # If Low E, will turn on light
            if(note == "Low E"):
                client.publish("macubero/callbackMic", "E")
            #if an A is played it will turn off the light
            elif (note == "A"):
                client.publish("macubero/callbackMic", "A")
            time.sleep(1)
        except KeyboardInterrupt:
            mic.mic_deit(stream)
            sys.exit()

