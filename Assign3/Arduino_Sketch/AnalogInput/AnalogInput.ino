/*
  
 */

int potentiometerPin = A0;    // select the input pin for the potentiometer
int ldrPin = A1;    // select the input pin for the LDR
int potentiometerVal = 0;
int ldrVal = 0;
int lowLDR = 0;  //calibration for normal light value; leave at 0 for calibration to determine
int highLDR = 0;  //calibration for normal light value; leave at 0 for calibration to determine
float midLDR =0;
int lowPotentiometer = 0;  //calibration for normal light value; leave at 0 for calibration to determine
int highPotentiometer = 0;  //calibration for normal light value; leave at 0 for calibration to determine
float midPotentiometer =0;

int calibration_time=15;

void setup() {
  
      lowLDR=9000;
      lowPotentiometer=9000;
      highLDR=0;
      highPotentiometer=0;
      
      unsigned long starttime = millis();
      unsigned long endtime = starttime;
      int analogLDRReading=0;
      int analogPotentiometerReading=0;
     
      while ((endtime - starttime) <=calibration_time*1000) // do this loop 20 Seconds
      {
        analogLDRReading=analogRead(ldrPin);
        analogPotentiometerReading=analogRead(potentiometerPin);
        
        if (analogLDRReading<lowLDR){ //recording the lowest value of LDR
          lowLDR=analogLDRReading;
        }
        
        if (analogLDRReading>highLDR){ //recording the highest value of LDR
          highLDR=analogLDRReading;
        }

        if (analogPotentiometerReading<lowPotentiometer){ //recording the lowest value of Potentiometer
          lowPotentiometer=analogPotentiometerReading;
        }
        
        if (analogPotentiometerReading>highPotentiometer){ //recording the highest value of Potentiometer
          highPotentiometer=analogPotentiometerReading;
        }
        
      endtime = millis();
      }
    
  Serial.begin(9600);

  Serial.print("Low LDR,");
  Serial.println(lowLDR);
  Serial.print("High LDR,");
  Serial.println(highLDR);
  
  Serial.print("Low Poten,");
  Serial.println(lowPotentiometer);
  Serial.print("High Poten,");
  Serial.println(highPotentiometer);
}

void loop() {
  // read the value from the sensor:
  potentiometerVal = analogRead(potentiometerPin);
  ldrVal = analogRead(ldrPin);

  //Serial.print("LDR - "); 
  Serial.println(ldrVal);
  //Serial.print("Potentiometer - ");
  Serial.println(potentiometerVal);
   
  // stop the program for 100 milliseconds:
  delay(100);
    
}
