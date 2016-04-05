 
raspberry.py does the following:

It subscribes to topics "lightSensor", "threshold", "lightStatus" and also publishes the status of rasberry pi after connecting to the broker (see on_connect())

It publishes either "TurnOn" or "TurnOff" to the topic "lightStatus" by comparing the lightSensor values to
the threshold value. see (on_message())

It also sets a last will info about rasberry pi status

