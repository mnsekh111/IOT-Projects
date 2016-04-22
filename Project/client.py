 
import time
import os,json
import ibmiotf.application
import uuid

client = None

try:
    options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")

    client = ibmiotf.application.Client(options)
    client.connect()
    print "Connect complete"
    while True:
                myData = {'buttonPushed' : True}
                client.publishEvent("RasPi", "b827ebaf79e5", "buttonPress", "json", myData)
                time.sleep(2.0)

except ibmiotf.ConnectionException  as e:
    print e
