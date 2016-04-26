from flask import Flask, redirect
from flask import render_template
from flask import request
import sys
import os, json
import time
import ibmiotf.application
from pfolder.svm import *
from pfolder.svmutil import *
import traceback

client = None
deviceId = os.getenv("DEVICE_ID")
vcap = json.loads(os.getenv("VCAP_SERVICES"))

# Global web app variables

close = 0
clear = 0
oopen = 0

result = "Unknown"

curr_data = ""

def my_callback(cmd):
    global curr_data
    global result

    if cmd.event == "SensorData":
        data = json.loads(cmd.payload)
        print data
        curr_data = str(data)
    try:      
        model = svm_load_model("svm.model")
        split_strings = curr_data.split(" ")
        test_data=[]
        tmp = {}
        tmp[1] = float(split_strings[0].split(":")[1])
        tmp[2] = float(split_strings[1].split(":")[1])
        tmp[3] = float(split_strings[2].split(":")[1])
        tmp[4] = float(split_strings[3].split(":")[1])
        tmp[5] = float(split_strings[4].split(":")[1])
        tmp[6] = float(split_strings[5].split(":")[1])
        test_data.append(tmp)
        
        plabels, p_acc, p_vals = svm_predict([0], test_data, model, options="")
        if int(plabels[0]) == -1:
            print "Close"
            result="Close"
        elif int(plabels[0]) == 1:
            print "Open"
            result="Open"

    except:
        traceback.print_exc()

try:
    options = {
        "org": vcap["iotf-service"][0]["credentials"]["org"],
        "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
        "auth-method": "apikey",
        "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
        "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
    }
    client = ibmiotf.application.Client(options)
    client.connect()
    os.chdir("pfolder")
    client.deviceEventCallback = my_callback
    client.subscribeToDeviceEvents(event="SensorData")

    print options

except ibmiotf.ConnectionException as e:
    print e

app = Flask(__name__)
if os.getenv("VCAP_APP_PORT"):
    port = int(os.getenv("VCAP_APP_PORT"))
else:
    port = 8080


@app.route('/')
def hello():
    return render_template("index.html")


def create_json():
    data = {}
    data['close'] = close
    data['open'] = oopen
    data['clear'] = clear
    return json.dumps(data)


@app.route('/ajax_send', methods=['POST'])
def ajax_send():
    global close, clear, oopen, result
    close = request.form['close']
    clear = request.form['clear']
    oopen = request.form['open']

    if close == "1":
        result = "Close"
    else:
        result = "Open"

    myData = create_json()
    print myData
    # client.publishEvent("RasPi", deviceId, "class", "json", myData)
    return ""


@app.route('/ajax_result', methods=['POST'])
def ajax_res():
    data = {}
    data["result"] = result
    data["data"] = curr_data
    output = "The data received is : " + curr_data + "\n The door is " + result
    #return json.dumps(data)
    return output


@app.route('/ajax_rec', methods=['POST'])
def ajax_rec():
    return create_json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
