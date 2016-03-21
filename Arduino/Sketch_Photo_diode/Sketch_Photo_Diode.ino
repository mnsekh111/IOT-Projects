/* Simple test of the functionality of the photo resistor

Connect the photodiode one leg to pin 0, and pin to +5V
Connect a resistor (around 10k is a good value, higher
values gives higher readings) from pin 0 to GND. (see appendix of arduino notebook page 37 for schematics).


----------------------------------------------------

                PhotoD     
 GND    o-------/\/\/----------.--o  Pin 0
                  |            | 
 GND    o---------|----/\/\/---|
                         10M
                             
----------------------------------------------------
*/

int lightPin = 0;  //define a pin for Photo resistor
int ledPin = 11;     //define a pin for LED
int normalLight = 0;  //calibration for normal light value

void setup()
{
    Serial.begin(9600);  //Begin serial communcation
    pinMode( ledPin, OUTPUT );
    delay(1000);//wait one second.
    int analogReading1=analogRead(lightPin);
    delay(1000);//wait one second.
    int analogReading2=analogRead(lightPin);
    delay(1000);//wait one second.
    int analogReading3=analogRead(lightPin);

    normalLight = (analogReading1+analogReading2+analogReading3)/3;
    Serial.print("debug: baseline set to:"); //Write the value of the photodiode to the serial monitor.
    Serial.println(normalLight); //Write the value of the photodiode to the serial monitor.

}

void loop()
{
    int analogReading=analogRead(lightPin);
    if (analogReading<normalLight*.80)
      Serial.print("off:"); //Write the value of the photodiode to the serial monitor.
    else if (analogReading>normalLight*1.20)
      Serial.print("on :"); //Write the value of the photodiode to the serial monitor.
    else
      Serial.print("???:"); //Write the value of the photodiode to the serial monitor.
    Serial.println(analogReading);          
    
    //analogWrite(ledPin, analogRead(lightPin)/2);  //send the value to the ledPin. Depending on value of resistor 
                                                //you have  to divide the value. for example, 
                                                //with a 10k resistor divide the value by 2, for 100k resistor divide by 4.
   delay(100); //short delay for faster response to light.
}
