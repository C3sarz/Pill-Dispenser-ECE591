#include "esp32-hal-cpu.h"
#include "analogWrite.h"

#define ENABLE_PIN 25
#define LASER_PIN 23
#define LASER_PHOTO_PIN 26
#define LASER_STATUS_PIN 16
#define CHAMBER_LED_PIN 22
#define CHAMBER_PHOTO_PIN 27
#define CHAMBER_STATUS_PIN 17


int chamberValue = 0;
int tripwireValue = 0;
bool tripped = false;

void setup() {
  setCpuFrequencyMhz(80); //Set CPU clock
  Serial.begin(115200);
  Serial.println("Begin!");
  pinMode(0, INPUT);
  pinMode(ENABLE_PIN, INPUT);
  pinMode(LASER_PHOTO_PIN, INPUT);
  pinMode(LASER_STATUS_PIN, OUTPUT);
  pinMode(CHAMBER_PHOTO_PIN, INPUT);
  pinMode(CHAMBER_STATUS_PIN, OUTPUT);
}

void loop() {

  if(digitalRead(ENABLE_PIN))
  {
    if(tripped) 
    {
      digitalWrite(LASER_STATUS_PIN, HIGH);      
      Serial.println("Tripped");
    }

    else
    {
      tripwireValue = analogRead(LASER_PHOTO_PIN);
      Serial.print("Laser photoresitor value: ");
      Serial.println(tripwireValue);
      if(tripwireValue <= 2300)
      {
        tripped = true;
      }
    }
  }
  else
  {    
    tripped = false;
    digitalWrite(LASER_STATUS_PIN, LOW);    
    if(chamberEmpty()) digitalWrite(CHAMBER_STATUS_PIN, HIGH);
    else digitalWrite(CHAMBER_STATUS_PIN, LOW);
  }
}

/* Returns TRUE if a pill is occupying the LED chamber. */
bool chamberEmpty()
{
  int value = 0;
  value = analogRead(CHAMBER_PHOTO_PIN);
  Serial.print("Chamber photoresitor value: ");
  Serial.println(value);
  if(value >= 100)
  {
    return true;
  }
  return false;
}
