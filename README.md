# GuitarProjectRPi
RPI

Team Members: Matthew Cubero and Seth Goolsby
Video Link: https://drive.google.com/file/d/1JTWyPygL7IHq2MMzHvmTciAnBAKqSiXi/view?usp=sharing

Instructions to Compile:
Must have a server up and running with Mosquitto. Have all the appropriate connections with each rpi_pub and rpi_led set. Just run rpi_pub.py on the Raspberry pi that has a USB mic attached, and rpi_led on an RPi with an LED attached.

The file MicToFTransform is called from rpi_pub and does most of the work to record and FFT, in this file, the Value dev_index is the index of the usb mic from the PyAudio function get_device_info_by_index()

Grovepi.py is used for the LED

usbMic.py and rpi_pub files are for testing. 

Libraries Used:
numpy
grovepi
paho
mosquitto
time