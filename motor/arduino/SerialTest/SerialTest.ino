
//Arduino Mega and Leonardo chips only support some pins for receiving data back from the RoboClaw
//This is because only some pins of these boards support PCINT interrupts or are UART receivers.
//Mega: 0,10,11,12,13,14,15,17,19,50,51,52,53,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15
//Leonardo: 0,8,9,10,11

//Arduino Due currently does not support SoftwareSerial. Only hardware uarts can be used, pins 0/1, 14/15, 16/17 or 18/19.

//Note: Most Arduinos do not support higher baudrates rates than 115200.  Also the arduino hardware uarts generate 57600 and 115200 with a
//relatively large error which can cause communications problems.

//See BareMinimum example for a list of library functions

//Includes required to use Roboclaw library
#include "BMSerial.h"
#include "RoboClaw.h"

//Roboclaw Address
#define address 0x80

//Setup communcaitions with roboclaw. Use pins 10 and 11 with 10ms timeout
RoboClaw roboclaw(10,11,10000);

void setup()
{
  //Open roboclaw serial ports
  roboclaw.begin(38400);
  
  Serial.begin(9600); // set the baud rate
  //Serial.println("Ready"); // print "Ready" once
}
void loop()
{
  char inByte = ' ';
  
  if(Serial.available()) // only send data back if data has been sent
  {
    char inByte = Serial.read(); // read the incoming data
    //Serial.println(inByte); // send the data back in a new line so that it is not all one long line
    if(inByte == '1')
    {
      Serial.print("drive motor");
      //drive the motor
      roboclaw.ForwardM1(address, 30);
      roboclaw.ForwardM2(address, 30);
      //Serial.println("driving motor");
      
    }
    else if (inByte == '0')
    {
      Serial.print("stop motor");
      roboclaw.ForwardM1(address, 0);
      roboclaw.ForwardM2(address, 0);
      //Serial.println("stopping motor");
    }
    else if(inByte == '2')
    {
      // right
      Serial.print("turning right");
      roboclaw.ForwardBackwardM1(address,30); //start Motor1 forward at half speed
      roboclaw.ForwardBackwardM2(address, 10); //start Motor2 backward at half speed
      
    }
    else if(inByte == '3')
    {
      Serial.println("turn left");
      roboclaw.ForwardBackwardM1(address,10);
      roboclaw.ForwardBackwardM2(address,30);
    }
    
  }
  

  
  delay(100); // delay for 1/10 of a second
}

