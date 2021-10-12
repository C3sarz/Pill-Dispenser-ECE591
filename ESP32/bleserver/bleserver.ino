#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
unsigned long time1, time2;
bool disp = false;

/* BLEServer *pServer = BLEDevice::createServer();
BLEService *pService = pServer->createService(SERVICE_UUID);
BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       ); */

BLEServer *pServer;
BLEService *pService;
BLECharacteristic *pCharacteristic;


void setup()
{
  Serial.begin(115200);
  Serial.println("Starting BLE Server!");

  BLEDevice::init("Dispenser-Server");
  pServer = BLEDevice::createServer();
  pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );

  
  /* BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );*/

  pCharacteristic->setValue("Dispenser Test");
  pService->start();
  //BLEAdvertising *pAdvertising = pServer->getAdvertising();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  //pAdvertising->start();
  Serial.println("Characteristic defined! Now you can read it in the Client!");
  pCharacteristic->setValue("normal");
  time1 = millis();
  time2 = time1;
  pinMode(0,INPUT);
  pinMode(2,OUTPUT);
}

void loop()
{
  if(disp == true && time1 + 3000 <= millis())
  {
    pCharacteristic->setValue("normal");
    std::string value = pCharacteristic->getValue();
    Serial.print("The new characteristic value is: ");
    Serial.println(value.c_str());
    digitalWrite(2,LOW);
    disp = false;
  }

  if(digitalRead(0) == false)
  {    
    pCharacteristic->setValue("dispensing");
    std::string value = pCharacteristic->getValue();
    Serial.print("The new characteristic value is: ");
    Serial.println(value.c_str());
    digitalWrite(2,HIGH);
    
    time1 = millis();
    time2 = time1;
    disp = true;
  }
  

}
