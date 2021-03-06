#EE 250 Project
# This node will only be able to see if the LED is on or off

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribing to hostname/topic
    client.subscribe("macubero/led")
    client.subscribe("macubero/callbackMic")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="ec2-3-138-142-104.us-east-2.compute.amazonaws.com", port=60000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        

