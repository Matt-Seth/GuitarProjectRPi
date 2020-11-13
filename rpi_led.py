#EE 250 Project 
# Will turn on or off an LED based off the commands sent by the other rpi
import paho.mqtt.client as mqtt
import time

led = 3
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribing to hostname/topic
    client.subscribe("macubero/led")
    client.subscribe("macubero/callbackMic")
    

#this will control our LED based off of the data from the mic
def callbackMic(client, userdata, msg):
    #if a Low E note is played will turn on the LED
    print("Incoming Message: " + (str(msg.payload, "utf-8")))
    if((str(msg.payload, "utf-8")) == "E"):
        digitalWrite(led,1)

    #if an A is played it will turn off the light
    elif ((str(msg.payload, "utf-8")) == "A"):
        digitalWrite(led,0)


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
        time.sleep(1)
        

