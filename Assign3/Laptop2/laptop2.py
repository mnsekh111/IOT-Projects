import paho.mqtt.client as paho
import time
import serial


#Get Serial connection    
ser = serial.Serial("/dev/ttyACM1", 9600)
lowLDR = 0
highLDR = 0
lowPotentiometer = 0
highPotentiometer = 0

prevLDR = 0
prevPotentiometer = 0



def on_publish(client, userdata, mid):
    print("userdata: "+str(userdata))

def on_message(client, userdata, msg):
    print("[" + time.ctime() + "] Topic = " + msg.topic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))
    global prevLDR    
    global prevPotentiometer
    if msg.topic == "lightSensor":
        prevLDR = int(msg.payload)
    if msg.topic == "threshold":
        prevPotentiometer = int(msg.payload)


def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.publish("status/Arduino", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2)])

def on_disconnect(client, userdata, rc):
    client.publish("status/Arduino", payload="Offline", qos=2, retain=True)



def getLimitValues():    
    print "In get Limit Values"
    global lowLDR
    global highLDR
    global lowPotentiometer
    global highPotentiometer
    lowLDR = int(ser.readline().split(',')[1])
    highLDR = int(ser.readline().split(',')[1])
    lowPotentiometer = int(ser.readline().split(',')[1])
    highPotentiometer = int(ser.readline().split(',')[1])

    print lowLDR
    print highLDR
    print lowPotentiometer
    print highPotentiometer
    print "Exit get limit values"

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


#Get high and low values for analog inputs
getLimitValues()

#Threshold set to 20%
thresholdLDR = (highLDR - lowLDR) * 0.2
thresholdPotentiometer = (highPotentiometer - lowPotentiometer) * 0.2

print "Threshold LDR"+ str(thresholdLDR)
print "Threshold Potentio"+ str(thresholdPotentiometer)

client.loop_start()

while 1:
    readLDR = int(ser.readline())
    readPotentiometer = int(ser.readline())
    print "LDR Value read "+str(readLDR)
    print "Potentiometer Value read "+str(readPotentiometer)

#Check if difference in previous and current LDR is more than the threshold. If yes, send a message
    if abs(readLDR - prevLDR) > thresholdLDR:
        print "Reached threshold for LDR. Send to topic"
        client.publish("lightSensor", payload=readLDR, qos=2, retain=True)
    if abs(readPotentiometer - prevPotentiometer) > thresholdPotentiometer:
        print "Reached threshold for Potentiometer. Send to topic"
        client.publish("threshold", payload=readPotentiometer, qos=2, retain=True)

    #prevLDR = readLDR
    #prevPotentiometer = readPotentiometer

client.loop_stop()
client.disconnect()

