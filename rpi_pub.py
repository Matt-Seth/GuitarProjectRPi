"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

from grovepi import*
from grove_rgb_lcd import*

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""

led = 3

def custom_callbackLCD(client, userdata, msg):
    setRGB(0,255,0)
    if str(msg.payload, "utf-8") != "":
        setText_norefresh("\n" + str(msg.payload, "utf-8"))

#this will control our LED based off of the data from the mic
def microphone_callback(client, userdata, msg):
    #if a Low E note is played will turn on the LED
    if((str(msg.payload, "utf-8")) == "Low E"):
        digitalWrite(led,1)

    #if an A is played it will turn off the light
    elif ((str(msg.payload, "utf-8")) == "A"):
        digitalWrite(led,0)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/led", callbackLED)
    client.subscribe("macubero/lcd")
    client.message_callback_add("macubero/lcd", callbackLCD)
    client.subscribe("macubero/led")
    client.message_callback_add("macubero/microphone", microphone_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    client.loop_start()

    while True:
        print("delete this line")
        #Sensor Readings
        try:
            #reading = ultrasonicRead(ultrasonic_ranger)
            # we'll do our mic function here

        except TypeError:
            print ("Error")
        except IOError:
            print ("Error")
        #button polling
        if digitalRead(buttonPin):
            client.publish("macubero/button", "Button pressed!")
        #publish URR
        #client.publish("macubero/ultrasonicRanger",str(reading))
        #1 second in between loops
        time.sleep(1)
            

