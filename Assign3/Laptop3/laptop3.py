import paho.mqtt.client as paho
import time

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: with QoS "+str(granted_qos))

#Print messages to console and log files
def on_message(client, userdata, msg):
    receivedTopic = msg.topic
    print("[" + time.ctime() + "] Topic = " + receivedTopic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))
    outputFile = open(receivedTopic.replace("\\",""),"a")
    outputFile.write("[" + time.ctime() + "] Topic = " + receivedTopic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))
    

def createLogFiles():
    lightSensorLog = open('lightSensor','w')
    thresholdLog = open('threshold','w')
    lightStatusLog = open('lightStatus','w')
    statusRpiLog = open('statusRaspi','w')
    statusArduinoLog = open('statusArduino','w')

createLogFiles()

#Create client
client = paho.Client("Laptop3")

#Add callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message

#Connect to the broker
client.connect("192.168.0.180", 1883)

#Subscribe to topics
client.subscribe("status/#", qos=2)
client.subscribe("lightSensor", qos=2)
client.subscribe("threshold", qos=2)
client.subscribe("lightStatus", qos=2)

client.loop_forever()
