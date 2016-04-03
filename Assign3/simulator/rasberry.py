import paho.mqtt.client as mqtt
        

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    
    client.publish("status/RaspPi", payload="Online", qos=2, retain=True)
    client.subscribe([("lightSensor",2),("threshold",2)])


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if msg.topic == "lightSensor":
            pass
        elif msg.topic == "threashold":
            pass

        #.
        #.
        #. Decision making
        #.
        #.
        lightStatus = "TurnOn"
        client.publish("LightStatus",payload=lightStatus,qos=2,retain=True)

def on_disconnect(client, userdata, rc):
    client.publish("status/RaspPi", payload="Offline", qos=2, retain=True)

client = mqtt.Client()
client.will_set("status/RaspPi", payload="Offline", qos=2, retain=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


