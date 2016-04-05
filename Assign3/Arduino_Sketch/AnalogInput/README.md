 
Before the sketch starts to loop, we caliberate the sensors for 15-20 sec inside the setup() module. After this the highest and
lowest readings of both potentiometer and LDR are sent to laptop 2 in the format 
'Low LDR,' lowLDRval
'High LDR, 'highLDRVal
'Low Poten,' lowPotenval
'High Poten,' highPotenVal

After thus, the arduino sketch repeatedly reads the analog pins to get the values of potentiometer and LDR and publishes it to the serial buffer.