/*
  Analog Input
 Demonstrates analog input by reading an analog sensor on analog pin 0 and
 turning on and off a light emitting diode(LED)  connected to digital pin 13.
 The amount of time the LED will be on and off depends on
 the value obtained by analogRead().

 The circuit:
 * Potentiometer attached to analog input 0
 * center pin of the potentiometer to the analog pin
 * one side pin (either one) to ground
 * the other side pin to +5V
 * LED anode (long leg) attached to digital output 13
 * LED cathode (short leg) attached to ground

 * Note: because most Arduinos have a built-in LED attached
 to pin 13 on the board, the LED is optional.


 Created by David Cuartielles
 modified 30 Aug 2011
 By Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/AnalogInput

 */

int potentiometerPin = A0;    // select the input pin for the potentiometer
int ldrPin = A1;    // select the input pin for the LDR
int potentiometerVal = 0;
int ldrVal = 0;
int normalLight = 0;  //calibration for normal light value; leave at 0 for calibration to determine
int highLight = 0;  //calibration for normal light value; leave at 0 for calibration to determine
float midway =0;
int calibration_time=10;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  potentiometerVal = analogRead(potentiometerPin);
  ldrVal = analogRead(ldrPin);

  Serial.print("Potentiometer - ");
   Serial.println(potentiometerVal);
  Serial.print("LDR - "); 
  Serial.println(ldrVal);
  // stop the program for 100 milliseconds:
  delay(1000);

    
}
