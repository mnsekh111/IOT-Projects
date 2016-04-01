import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: with QoS "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


#Create client
client = paho.Client("Laptop3")

#Add callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message

#Connect to the broker
client.connect("192.168.0.238", 1883)

#Subscribe to topics
client.subscribe("status/#", qos=2)
client.subscribe("sensors/#", qos=2)

client.loop_forever()