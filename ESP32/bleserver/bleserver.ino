#include <BLEDevice.h>
#include "esp32-hal-cpu.h"
#include "analogWrite.h"
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Esp.h>
#include <esp_system.h>
#include <sys/time.h>

#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  3        /* Time ESP32 will go to sleep (in seconds) */

#define MOTOR_PIN 17  /* Pin for the vibration motor */
#define LED1_PIN 26      /* Pin for LED 1 */
#define LED2_PIN 27      /* pin for LED 2 */

// RTC Code
//struct timeval tv;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define BRACELET_SERVICE_UUID     "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define ALERT_SERVICE_UUID        "ad7cb91c-a5b2-406c-b3ee-f7f012d695d5"


#define CHARACTERISTIC_UUID       "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define NEXT_DISPENSE_TIME_UUID   "58aeaf50-462d-44d0-8126-4a67a94d0f13"
#define RTC_TIME_UUID             "96a70179-ecff-4ac1-a77e-fbb455642469"
#define BATTERY_PERCENT_UUID      "bd56315d-307c-4e55-87f7-9aa97dcab6e4"
#define VIBRATION_INTENSITY_UUID  "f92ac116-5f97-4603-8e3d-1867a7c11521"

unsigned long dispTimer = 0;
unsigned long timer1 = 0;
static bool disp = false;
static bool vibrating = false;
bool isConnected = false;
unsigned int dispCount = 0;
static char serverMessage[1000] = "defaultValue";

BLEServer *pServer;
BLEService *pAlertService;
BLEService *pBraceletService;
BLECharacteristic *pCharacteristic;

class ServerCallback : public BLEServerCallbacks
{
  void onConnect(BLEServer *pServer)
  {
    
    isConnected = true;
    analogWrite(LED2_PIN, 10);
  }

  void onDisconnect(BLEServer *pServer)
  {
    isConnected = false;
    analogWrite(LED2_PIN, 0);
    Serial.println("onDisconnect");
    BLEDevice::startAdvertising();
    pCharacteristic->setValue("normal");
  }
};

void setup()
{
  /* Set up the serial connection and the ESP32 */
  Serial.begin(115200);
  Serial.print("Starting Alert Bracelet BLE Server with CPU @ ");
  setCpuFrequencyMhz(80); //Set CPU clock
  Serial.print(getCpuFrequencyMhz());
  Serial.println("MHz.");

  /* Sleep configuration */
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("Sleep constant set to " + String(TIME_TO_SLEEP) +
  " Seconds.");

   /* Set up peripheral pins */
  pinMode(MOTOR_PIN, OUTPUT); 
  pinMode(LED1_PIN, OUTPUT); 
  pinMode(LED2_PIN, OUTPUT);  
  pinMode(0, INPUT);
  
  BLEDevice::init("Alert-Bracelet");
  pServer = BLEDevice::createServer();  
  pAlertService = pServer->createService(ALERT_SERVICE_UUID);  
  pBraceletService = pServer->createService(BRACELET_SERVICE_UUID);
  pCharacteristic = pAlertService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pAlertService->start();
  //BLEAdvertising *pAdvertising = pServer->getAdvertising();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(BRACELET_SERVICE_UUID);
  pAdvertising->addServiceUUID(ALERT_SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  pServer->setCallbacks(new ServerCallback());
  BLEDevice::startAdvertising();
  //pAdvertising->start();
  Serial.println("Characteristic defined! Now you can read it in the Client!");
  pCharacteristic->setValue("normal");
  timer1 = millis();
}

void loop()
{

    if(isConnected)
    {
      /* Read remote characteristic to determine if dispensing is taking place */
      strcpy(serverMessage, pCharacteristic->getValue().c_str());
      Serial.print("Received message from server: ");
      Serial.println(serverMessage);
  
      if (!disp && String(serverMessage).equals("dispensing"))
      {
        vibrating = true;
        dispTimer = millis();
        disp = true;
      }  
    }


  
  //Dispensing command received
  if(disp)
  {
    if(dispTimer + 1000 <= millis())
    {
      if(vibrating)
      {
        analogWrite(LED1_PIN, 10);
        analogWrite(MOTOR_PIN, 255/2);
      }
      else
      {
        analogWrite(LED1_PIN, 0);
        analogWrite(MOTOR_PIN, 0);
      }
      vibrating = !vibrating;
      dispCount++;
      dispTimer = millis();
    }
    
    if(dispCount >= 6)
    {
      analogWrite(LED1_PIN, 0);
      analogWrite(MOTOR_PIN, 0);
      disp = false;
      dispCount = 0;
    }
  }

  delay(500);
//  if(disp == true && time1 + 3000 <= millis())
//  {
//    pCharacteristic->setValue("normal");
//    std::string value = pCharacteristic->getValue();
//    Serial.print("The new characteristic value is: ");
//    Serial.println(value.c_str());
//    digitalWrite(2,LOW);
//    disp = false;
//  }
//
//  if(digitalRead(0) == false)
//  {    
//    pCharacteristic->setValue("dispensing");
//    std::string value = pCharacteristic->getValue();
//    Serial.print("The new characteristic value is: ");
//    Serial.println(value.c_str());
//    digitalWrite(2,HIGH);
//    
//    time1 = millis();
//    time2 = time1;
//    disp = true;
//  }
  

}
