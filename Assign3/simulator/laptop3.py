import paho.mqtt.client as paho
import time

lightSensorLog = None
thresholdLog = None
lightStatusLog = None
statusRpiLog = None
statusArduinoLog = None


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: with QoS " + str(granted_qos))


# Print messages to console and log files
def on_message(client, userdata, msg):
    receivedTopic = msg.topic
    fileName = sanitizeFileName(receivedTopic);
    content_write = "\n[" + time.ctime() + "] Topic = " + receivedTopic + ", QoS = " + str(
        msg.qos) + ", Payload = " + str(msg.payload)

    print(content_write)
    if fileName == "statusArduino":
        statusArduinoLog.write(content_write)
    elif fileName == "statusRaspi":
        statusRpiLog.write(content_write)
    elif fileName == "lightStatus":
        lightStatusLog.write(content_write)
    elif fileName == "lightSensor":
        lightSensorLog.write(content_write)
    elif fileName == "threshold":
        thresholdLog.write(content_write)


def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to topics
    client.subscribe("status/#", qos=2)
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)
    client.subscribe("lightStatus", qos=2)


def on_disconnect(client, userdata, rc):
    lightSensorLog.close()
    thresholdLog.close()
    lightStatusLog.close()
    statusRpiLog.close()
    statusArduinoLog.close()


def createLogFiles():
    lightSensorLog = open('lightSensor', 'a')
    thresholdLog = open('threshold', 'a')
    lightStatusLog = open('lightStatus', 'a')
    statusRpiLog = open('statusRaspi', 'a')
    statusArduinoLog = open('statusArduino', 'a')


def sanitizeFileName(input):
    return input.replace("\\", "").replace("/", "")


createLogFiles()

# Create client
client = paho.Client("Laptop3")

# Add callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the broker
client.connect("192.168.0.180", 1883, keepalive=10)

client.loop_forever()
