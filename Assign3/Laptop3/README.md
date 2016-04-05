 


laptop3.py does the following things:

It Subscribes to all the topics (see on_connect())

It creates log files for all the topics it is listening to (see createLogFiles())

It keeps appending data to those files once some data is published to those topics (see on_message())
