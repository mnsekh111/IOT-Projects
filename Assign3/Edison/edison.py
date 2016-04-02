import paho.mqtt.client as paho
import time
import mraa

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: with QoS "+str(granted_qos))

#Print messages to console and log files
def on_message(client, userdata, msg):
    print("[" + time.ctime() + "] Topic = " + receivedTopic + ", QoS = " 
+ str(msg.qos)+", Payload = "+str(msg.payload))

#Set Output Led status
    if msg.topic == "lightStatus":
        if msg.payload == "Turn On":
            outputStatus = True
        else:
            outputStatus = False

#Set Raspberry Led status
    if msg.topic == "status/rpi":
        if msg.payload == "Connect":
            rpiStatus = True
        else:
            rpiStatus = False

#Set Arduino Led status
    if msg.topic == "arduinoStatus":
        if msg.payload == "Connect":
            arduinoStatus = True
        else:
            arduinoStatus = False


def ledAction():
    if arduinoStatus:
        print "toggle arduino led on"
        arduinoLed.write(1)
    else:
        print "toggle arduino led off"
        arduinoLed.write(0)

    if rpiStatus:
        print "toggle rpi led on"
        rpiLed.write(1)
    else:
        print "toggle rpi led off"
        print "toggle output led off"
        rpiLed.write(0)
        arduinoLed.write(0)

    if rpiStatus and outputStatus:
        print "toggle output led on"
        outputLed.write(1)
    else:
        print "toggle output led off"
        outputLed.write(0)

#initialize Mraa
rpiLed = mraa.Gpio(36)
arduinoLed = mraa.Gpio(48)
outputLed = mraa.Gpio(14)
rpiLed.dir(mraa.DIR_OUT)
arduinoLed.dir(mraa.DIR_OUT)
outputLed.dir(mraa.DIR_OUT)
rpiLed.write(0)
arduinoLed.write(0)
outputLed.write(0)

rpiStatus = False
arduinoStatus = False
outputStatus = False

#Create client
client = paho.Client("Edison")

#Add callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message

#Connect to the broker
client.connect("192.168.0.180", 1883)

#Subscribe to topics
client.subscribe("status/#", qos=2)
client.subscribe("lightStatus", qos=2)

client.loop_forever()
