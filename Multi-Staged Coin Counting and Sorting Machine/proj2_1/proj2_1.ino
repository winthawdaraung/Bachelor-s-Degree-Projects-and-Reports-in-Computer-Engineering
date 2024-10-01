#define IR_SENSOR_PIN0 0
#define IR_SENSOR_PIN1 1
#define IR_SENSOR_PIN2 2
#define LED_PIN 13    
#include <Servo.h>
 
//HX711
















































































#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
 
//LCD
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
 
int counter0 = 0;  
int counter1 = 0;
int counter2 = 0;  
 
 
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
 
int pos = 0;
int pos1 = 0;
float wiper_weight = 0;
 
 
const int threshold = 500; // Adjust this value based on your sensor setup
 
//LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);
 
//HX711
const int HX711_dout = 4; //mcu > HX711 dout pin
const int HX711_sck = 5;
float stabilityThreshold = 0.1;
float lastStableWeight = 0.0;
float previousWeight = 0.0;
int stableCount = 0;
static boolean readnewdata = true;
 
HX711_ADC LoadCell(HX711_dout, HX711_sck);
 
 
 
const int calVal_eepromAdress = 0;
unsigned long t = 0;
 
 
void setup() {
//LCD
  Serial.begin(57600); delay(10);
  Serial.println();
  Serial.println("Starting...");
 
  // Serial.begin(9600);   // Initialize serial communication
  pinMode(IR_SENSOR_PIN0, INPUT);
  pinMode(IR_SENSOR_PIN1, INPUT);
  pinMode(IR_SENSOR_PIN2, INPUT);
  pinMode(LED_PIN, OUTPUT); // Set LED pin as output (optional)
 
 
 
  servo1.attach(9);
  servo2.attach(11);
  servo3.attach(6);
  servo4.attach(10);
 
  lcd.init();         // initialize the lcd
  lcd.backlight();
 
  //HX711
  LoadCell.begin();
 
  float calibrationValue; // calibration value (see example file "Calibration.ino")
  calibrationValue = 696.0; // uncomment this if you want to set the calibration value in the sketch
  EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom
 
  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
    Serial.println("Startup is complete");
  }
}
 
 
void loop() {
  int sensorValue0 = analogRead(IR_SENSOR_PIN0);
  int sensorValue1 = analogRead(IR_SENSOR_PIN1);
  int sensorValue2 = analogRead(IR_SENSOR_PIN2);
 
 
 
  lcd.setCursor(0, 0);
  lcd.print("  1B   5B  10B  ");
 
 
  lcd.setCursor(3, 1);
  lcd.print(counter0);
  lcd.setCursor(8, 1);
  lcd.print(counter1);
  lcd.setCursor(13, 1);
  lcd.print(counter2);
 
  static boolean newDataReady = 0;
  const int serialPrintInterval = 500; //increase value to slow down serial print activity
  const int stabilityThresholdCount = 3; // Number of stable readings required for stability
 
   if(readnewdata){
    if (LoadCell.update()) {newDataReady = true;}
  }
 
  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
     
      float currentWeight = LoadCell.getData();
      currentWeight = currentWeight-wiper_weight;
      Serial.print("Load_cell output val: ");
      Serial.println(currentWeight);  
      currentWeight = currentWeight-wiper_weight;
    
      t = millis();
      if (abs(currentWeight - previousWeight) < stabilityThreshold){
        stableCount++;
        // Serial.println(stableCount);
        if (stableCount >= stabilityThresholdCount){
          // Weight reading is stable
          lastStableWeight = currentWeight;
          stableCount = 0; // Reset the stable count
          Serial.print("Stable val: ");
          Serial.println(lastStableWeight);
 
          if (lastStableWeight >= 2.5 && lastStableWeight < 3.5){
            for (; pos <= 90; pos += 1)
              {
                servo1.write(pos);
                delay(5);              
              }
            readnewdata = false;
            for (; pos1 <= 45; pos1 += 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
            delay(500);
            for (; pos1 >= -10; pos1 -= 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
          }
          else if (lastStableWeight >= 5.8 && lastStableWeight < 6.5){
            for (; pos <= 90; pos += 1)
            {
              servo2.write(pos);  
              delay(5);            
            }
            readnewdata = false;
            for (; pos1 <= 45; pos1 += 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
            delay(500);
            for (; pos1 >= -10; pos1 -= 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
          }
          else if (lastStableWeight >= 7.8 && lastStableWeight < 8.8)
          {
            for (; pos <= 90; pos += 1)
              {
                servo3.write(pos);  
                delay(5);        
              }
            readnewdata = false;
            for (; pos1 <= 45; pos1 += 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
            delay(500);
            for (; pos1 >= -10; pos1 -= 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
 
          }
          else if (lastStableWeight > 0.1){
            for (; pos1 <= 45; pos1 += 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
            delay(500);
            for (; pos1 >= -10; pos1 -= 1)
            {
              servo4.write(pos1);  
              delay(7);            
            }
          }
          else
          {
            servo1.write(0);
            servo2.write(0);
            servo3.write(0);
            servo4.write(-10);
          }
        }
      }
      else
      {
        stableCount = 0;
      }
      previousWeight = currentWeight;
    }
 
  }
 
 
  // Check if sensor value is below threshold (indicating object interrupting beam)
  if ((sensorValue0 < threshold) || (sensorValue1 < threshold)|| (sensorValue2 < threshold))
  {
      if (sensorValue0 < threshold) {
    counter0++; // Print message to serial monitor
    // digitalWrite(LED_PIN, HIGH);    // Turn on LED (optional)
    delay(500);                       // Delay to avoid multiple counts for a single coin
    for (; pos >= 0; pos -= 1)
      {
      servo1.write(pos);
      delay(5);              
      }
      delay(1000);
    readnewdata = true;
 
  }
  else if((sensorValue1 < threshold))
  {
    counter1++;
 
 
    delay(500);
     for (; pos >= 0; pos -= 1)
      {
      servo2.write(pos);
      delay(5);              
      }
      delay(1000);
    readnewdata = true;
  }
    else if((sensorValue2 < threshold))
  {
    counter2++;
 
    delay(500);
     for (; pos >= 0; pos -= 1)
      {
      servo3.write(pos);
      delay(5);              
      }
      delay(1000);
    readnewdata = true;
 
  }
 
 
  Serial.println("Counter0 = "+ String(counter0) + " Counter1= "+ String(counter1)+ " Counter2= "+ String(counter2));
 
  }
   
}