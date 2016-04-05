import paho.mqtt.client as paho
import time
import serial

#Get Serial connection    
ser = serial.Serial("/dev/ttyACM1", 9600)

#Initialize global values
lowLDR = 0
highLDR = 0
lowPotentiometer = 0
highPotentiometer = 0
prevLDR = 0
prevPotentiometer = 0


#Function to normalize between 0-10
def normalize(inputValue, minValue, maxValue):
    return 10*(inputValue-minValue)/(maxValue-minValue)

#Function to normalize between 0-10
def denormalize(inputValue, minValue, maxValue):
    return (inputValue*(maxValue-minValue) + 10*minValue)/10


#Paho handlers
def on_publish(client, userdata, mid):
    print("Publishing value on  mid - "+str(mid))

def on_message(client, userdata, msg):
    print("Received message at [" + time.ctime() + "] Topic = " + msg.topic + ", QoS = " + str(msg.qos)+", Payload = "+str(msg.payload))
    global prevLDR    
    global prevPotentiometer
    if msg.topic == "lightSensor":
        prevLDR = denormalize(int(msg.payload),lowLDR,highLDR)
    if msg.topic == "threshold":
        prevPotentiometer = denormalize(int(msg.payload),lowPotentiometer,highPotentiometer)
    print "De normalized prev LDR - " + str(prevLDR)
    print "De normalized prev Poten - " + str(prevPotentiometer)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.publish("status/Arduino", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2)])

def on_disconnect(client, userdata, rc):
    client.publish("status/Arduino", payload="Offline", qos=2, retain=True)

#Initial Calibration step. Get max and min values for LDR and Potentiometer
def getLimitValues():    
    global lowLDR
    global highLDR
    global lowPotentiometer
    global highPotentiometer
    lowLDR = int(ser.readline().split(',')[1])
    highLDR = int(ser.readline().split(',')[1])
    lowPotentiometer = int(ser.readline().split(',')[1])
    highPotentiometer = int(ser.readline().split(',')[1])

    print "Low LDR - " + str(lowLDR)
    print "High LDR - " + str(highLDR)
    print "Low Potentiometer - " + str(lowPotentiometer)
    print "High Potentiometer - " + str(highPotentiometer)


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
client.connect("192.168.0.180", 1883, keepalive=30)

#Get high and low values for analog inputs
getLimitValues()

#Threshold set to 20%
thresholdLDR = (highLDR - lowLDR) * 0.2
thresholdPotentiometer = (highPotentiometer - lowPotentiometer) * 0.2
print "Threshold LDR"+ str(thresholdLDR)
print "Threshold Potentio"+ str(thresholdPotentiometer)

client.loop_start()

#Read values from Arduino. If value > threshold, normalize to 0-10 and publish to the broker
while 1:
    readLDR = int(ser.readline())
    readPotentiometer = int(ser.readline())
    print "LDR Value read "+str(readLDR)
    print "Potentiometer Value read "+str(readPotentiometer)

#Check if difference in previous and current LDR is more than the threshold. If yes, normalize and publish
    if abs(readLDR - prevLDR) > thresholdLDR:
        print "Reached threshold for LDR. Send to topic"
        client.publish("lightSensor", payload=normalize(readLDR,lowLDR,highLDR), qos=2, retain=True)
    if abs(readPotentiometer - prevPotentiometer) > thresholdPotentiometer:
        print "Reached threshold for Potentiometer. Send to topic"
        client.publish("threshold", payload=normalize(readPotentiometer,lowPotentiometer,highPotentiometer), qos=2, retain=True)

client.loop_stop()

client.disconnect()
