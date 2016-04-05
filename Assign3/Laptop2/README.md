

laptop2.py does the following things:
 
It reads the LDR and potentiometer values (both the initial setup values (see getLimitValues()) and the continous values (see the while(1) loop) ) published by Arduino from the serial port. 

It Subscribes to specified topics and also publishes the status of arduino after connecting to the broker (see on_connect())

It also sets a last will info about Arduino status. 

It uses the funtion normalize() to convert the values into range 0-10.

It also keeps track of the previously published potentiometer and LDR values (see on_message())

It compares the read values with the previous values if the difference in greater than a particular threshold, then it publishes those values again to the specified topics
(see the while(1) loop  )

