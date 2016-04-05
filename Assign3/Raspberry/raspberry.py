import paho.mqtt.client as paho
import time

listSensorValue = 0
thresholdValue = 0
previousMessage = ""

def on_publish(client, userdata, mid):
    print("Publishing value on mid - "+str(mid))


def on_message(client, userdata, msg):
    print("Received message at [" + time.ctime() + "] Topic = " + msg.topic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))
    global listSensorValue    
    global thresholdValue
    global previousMessage
    if msg.topic == "lightSensor":
        listSensorValue = int(msg.payload)
    if msg.topic == "threshold":
        thresholdValue = int(msg.payload)
    if msg.topic == "lightStatus":
        previousMessage = msg.payload
        return

#If light is dim, turn on the led. Else turn off the led. Dont publish duplicate message. 
    if listSensorValue <= thresholdValue:
        if previousMessage != "Turn On":
            print "Publish light on"
            client.publish("lightStatus", payload="Turn On", qos=2, retain=True)
    else:
        if previousMessage != "Turn Off":
            print "Publish light on"
            client.publish("lightStatus", payload="Turn Off", qos=2, retain=True)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.publish("status/Raspi", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2),("lightStatus",2)])

def on_disconnect(client, userdata, rc):
    client.publish("status/Raspi", payload="Offline", qos=2, retain=True)


#Create client
client = paho.Client("RaspberryPi")

#Set Last Will to send "Offline" before disconnecting
client.will_set("status/Raspi", payload="Offline", qos=2, retain=True)

#Set callbacks
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

#Connect to Broker
client.connect("192.168.0.180", 1883)

client.loop_forever()
