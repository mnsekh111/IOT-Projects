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
float midway =0;
int calibration_time=10;

void setup()
{
    Serial.begin(9600);  //Begin serial communcation
    pinMode( ledPin, OUTPUT );
    
    Serial.print("calibration starting. you have ");
    Serial.print(calibration_time);
    Serial.println(" seconds to show the photodiode an example of off and on."); //


    if (normalLight==0 or highLight==0){
      normalLight=9000;
      unsigned long starttime = millis();
      unsigned long endtime = starttime;
      int analogReading=0;
      while ((endtime - starttime) <=calibration_time*1000) // do this loop 20 Seconds
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

    midway=(highLight-normalLight)/2 + normalLight;
    Serial.print("debug: normalLight set to:"); //
    Serial.println(normalLight); //
    Serial.print("debug: highLight set to:"); 
    Serial.println(highLight); 
    Serial.print("debug: midway set to:"); //
    Serial.println(midway); //

}

void loop()
{
    int analogReading=analogRead(lightPin);
    if (analogReading<midway)
      Serial.print("0"); //Write the value of the photodiode to the serial monitor.
    else if (analogReading>midway)
      Serial.print("1"); //Write the value of the photodiode to the serial monitor.
//    else
//      Serial.print("???:"); //Write the value of the photodiode to the serial monitor.
//    Serial.print(":");          
//    Serial.println(analogReading);          
    
   delay(100); //short delay for faster response to light.
}
