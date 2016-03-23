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
int normalLight = 0;  //calibration for normal light value; leave at 0 for calibration to determine
int highLight = 0;  //calibration for normal light value; leave at 0 for calibration to determine
float normal_tolerance = 1.30; //if light is less than 70% normal, then low
float high_tolerance =  0.70; //if light is more than 90% highest, then high


void setup()
{
    Serial.begin(9600);  //Begin serial communcation
    pinMode( ledPin, OUTPUT );
    


    if (normalLight==0){
      normalLight=9000;
      unsigned long starttime = millis();
      unsigned long endtime = starttime;
      int analogReading=0;
      while ((endtime - starttime) <=20*1000) // do this loop 20 Seconds
      {
        analogReading=analogRead(lightPin);
        if (analogReading<normalLight){ //recording the lowest value of light
          normalLight=analogReading;
        }
        if (analogReading>highLight){ //recording the highest value of light
          highLight=analogReading;
        }
      endtime = millis();
      }
    }
    
    Serial.print("debug: normalLight set to:"); //
    Serial.println(normalLight); //
    Serial.print("debug: highLight set to:"); 
    Serial.println(highLight); 
    Serial.print("debug: normalLight tolerance set to:"); //
    Serial.println(normalLight*normal_tolerance); //
    Serial.print("debug: highLight tolerance set to:"); //
    Serial.println(normalLight*high_tolerance); //

}

void loop()
{
    int analogReading=analogRead(lightPin);
    if (analogReading<normalLight*normal_tolerance)
      Serial.print("off:"); //Write the value of the photodiode to the serial monitor.
    else if (analogReading>highLight*high_tolerance)
      Serial.print("on :"); //Write the value of the photodiode to the serial monitor.
    else
      Serial.print("???:"); //Write the value of the photodiode to the serial monitor.
    Serial.println(analogReading);          
    
   delay(100); //short delay for faster response to light.
}
