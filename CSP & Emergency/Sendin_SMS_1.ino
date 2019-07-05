#include <SoftwareSerial.h>

//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(3, 2); //SIM800L Tx & Rx is connected to Arduino #3 & #2

void setup()
{
  Serial.begin(9600);
  while(!Serial.available()){
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  mySerial.begin(4800);
  int y =  Serial.read();
  Serial.print(y);
  delay(1000);
  mySerial.write(y);
  mySerial.print(y);
  
  //Begin serial communication with Arduino and Arduino IDE (Serial Monitor)

  Serial.println("Initializing..."); 
  delay(1000);

  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  updateSerial();
  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+CMGS=\"+201124335044\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  updateSerial();
  mySerial.write(y);
  if (y == 0){
  mySerial.print("There has been a crash and the severity is Non-Fatal"); //text content
  } 
  if (y == 1){
  mySerial.print("There has been a crash and the severity is Medium"); //text content  } 
  }
  if (y == 2){
  mySerial.print("There has been a crash and the severity is Super"); //text content  } 
  }
  if (y == 3){
  mySerial.print("There has been a crash and the severity is Fatal"); //text content  } 
  }
  mySerial.write(26);

}


void loop()
{
}

void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) 
  {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}

