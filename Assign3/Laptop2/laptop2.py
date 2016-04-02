import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

#Create client
client = paho.Client("Laptop2")

#Set Last Will to send "Offline" before disconnecting
client.will_set("status/Arduino", payload="Offline", qos=2, retain=True)

#Set callbacks
client.on_publish = on_publish

#Connect to Broker
client.connect("192.168.0.180", 1883)

#Publish an "Online" message
client.publish("status/Arduino", payload="Online", qos=2, retain=True)

client.loop_forever()
