import paho.mqtt.client as paho
import time
import serial

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_message(client, userdata, msg):
    print("[" + time.ctime() + "] Topic = " + msg.topic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))


def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.publish("status/Arduino", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2)])

def on_disconnect(client, userdata, rc):
    client.publish("status/Arduino", payload="Offline", qos=2, retain=True)


#Get Serial connection
ser = serial.Serial('COM3', 9600, timeout=0)
print ser.readline()


#Create client
client = paho.Client("Laptop2")

#Set Last Will to send "Offline" before disconnecting
client.will_set("status/Arduino", payload="Offline", qos=2, retain=True)

#Set callbacks
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

#Connect to Broker
client.connect("192.168.0.180", 1883)

client.loop_forever()


