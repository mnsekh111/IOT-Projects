import paho.mqtt.client as mqtt
import threading
import time
import random

#Thread that generates data
def arduino_simulator(client,delay,msg_count):
    cnt = 0
    while cnt < msg_count:
        print "%s %d" % ("dummy message" ,cnt)
        time.sleep(delay)
        cnt += 1
        client.publish("lightSensor",payload = random.randint(0,100)/100.0,qos=2,retain=True)
        client.publish("threshold",payload = random.randint(0,100)/100.0,qos=2,retain=True)
    print "Exiting thread"
        

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    
    client.publish("status/Arduino", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2)])
    thread1 = threading.Thread(name="runner",target = arduino_simulator(client,1,5))


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

def on_disconnect(client, userdata, rc):
    client.publish("status/Arduino", payload="Offline", qos=2, retain=True)

client = mqtt.Client()
client.will_set("status/Arduino", payload="Offline", qos=2, retain=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)



client.loop_forever()


