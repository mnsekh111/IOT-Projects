import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

#Create client
client = paho.Client("RaspberryPi")

#Set Last Will to send "Offline" before disconnecting
client.will_set("status/raspi", payload="Offline", qos=2, retain=True)

#Set callbacks
client.on_publish = on_publish

#Connect to Broker
client.connect("192.168.0.238", 1883)
client.loop_start()

#Publish an "Online" message
client.publish("status/raspi", payload="Online", qos=2, retain=True)

while True:
    time.sleep(30)