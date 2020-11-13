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

def callbackLED(client, userdata, msg):
    #conditions for turning on and off the LED
    # just an update on the LED status on the other rpi
    print(str(msg.payload, "utf-8"))

def callbackMic(client, userdata, msg):
    # just an update on what note was played and the command sent
    print(str(msg.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    # we are going to subscribe to the led topic to get the status of the led
    # we are going to subscribe to microphone so we can see what note we played
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/led", callbackLED)
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/microphone", callbackMic)

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
    
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    
    """ These functions implement a threaded interface to the network loop. 
    Calling loop_start() once, before or after connect*(), runs a thread in the 
    background to call loop() automatically. This frees up the main thread for other 
    work that may be blocking. This call also handles reconnecting to the broker. 
    Call loop_stop() to stop the background thread. The force argument is currently ignored.
    """
    client.loop_start()
    stream = mic.mic_init()

    while True:
        #Sensor Readings
        try:
            note = ""
            #try:
            #we'll do our mic function here
            note = mic.getNote(stream)
            print(note)
            #except TypeError:
            #   print ("Error TypeError")
            #except IOError:
            #   print ("Error ")
            if(note == "Low E"):
                client.publish("macubero/callbackMic", "E")

            #if an A is played it will turn off the light
            elif (note == "A"):
                client.publish("macubero/callbackMic", "A")

                #1 second in between loops
            time.sleep(1)
        except KeyboardInterrupt:
            mic.mic_deit(stream)
            sys.exit()

