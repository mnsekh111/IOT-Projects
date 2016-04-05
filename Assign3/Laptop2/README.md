
 
Laptop 2 reads the LDR and potentiometer values (both the initial setup values and the continous values ) published by Arduino from the serial port. 

It uses the funtion normalize() to convert the values into range 0-10.

It also keeps track of the previously published potentiometer and LDR values (See on_message())

It compares the read values with the previous values if the difference in greater than a particular threshold, then it publishes those values again to the specified topics
(see the while(1) loop in laptop2.py)