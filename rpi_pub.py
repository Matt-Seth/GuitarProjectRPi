"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi', by giving the path below
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

from grovepi import*
from grove_rgb_lcd import*

led = 3

#this will control our LED based off of the data from the mic
def microphone_callback(client, userdata, msg):
    #if a Low E note is played will turn on the LED
    if((str(msg.payload, "utf-8")) == "Low E"):
        digitalWrite(led,1)

    #if an A is played it will turn off the light
    elif ((str(msg.payload, "utf-8")) == "A"):
        digitalWrite(led,0)
def custom_callbackLED(client, userdata, msg):
    print("Custom Callback for LED")
    #conditions for turning on and off the LED
    if ((str(msg.payload, "utf-8")) == "LED_ON"):
        digitalWrite(led,1)

    elif ((str(msg.payload, "utf-8")) == "LED_OFF"):
        digitalWrite(led,0)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    # we are going to subscribe to the led topic to get the status of the led
    # we are going to subscribe to microphone so we can see what note we played
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/led", callbackLED)
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/microphone", microphone_callback)

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

    while True:
        #Sensor Readings
        # try:
        #     #reading = ultrasonicRead(ultrasonic_ranger)
        #     # we'll do our mic function here

        # except TypeError:
        #     print ("Error")
        # except IOError:
        #     print ("Error")

        client.publish("macubero/led","LED_OFF")

        #1 second in between loops
        time.sleep(1)
            

