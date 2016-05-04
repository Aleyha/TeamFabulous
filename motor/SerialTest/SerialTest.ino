
#include <Sabertooth.h>


#define middleSignal 5 // signal from main that shows straight turn
#define motorGradient 9// difference for each level of turning, e.g. 64 to a motor plus a motorGradient of 5 = 69
#define gradientRange 4 // difference between middle and either max or min.  e.g. middle is 5, max is 9, gR = 4
#define neutral 0 // signal for ForwardBackward to not turn either way
#define fuckedUpMotorOffset 0.85 // one motor sucks so this is the offset
#define spinSpeed 35  // speed for spin per motor (one's neg one's pos)
#define reverseSpeed 40 // speed for full reverse

Sabertooth ST(128);

void setup()
{
  SabertoothTXPinSerial.begin(9600);
 ST.autobaud();
  
  Serial.begin(9600); // set the baud rate
  ST.setRamping(7);
  //Serial.println("Ready"); // print "Ready" once
}
void loop()
{
  char inByte = ' ';
  
  if(Serial.available()) // only send data back if data has been sent
  {
    char inByte = Serial.read(); // read the incoming data
    //Serial.println(inByte); // send the data back in a new line so that it is not all one long line

	
    // single digits only

    if(inByte == 'a') {
      ST.motor(1, -1 * reverseSpeed * fuckedUpMotorOffset);
      ST.motor(2, -1 * reverseSpeed);
    }
    if(inByte == 'b') {
      ST.motor(1, spinSpeed * fuckedUpMotorOffset);
      ST.motor(2, -1 * spinSpeed);
    }
    if(inByte == 'c') {
      ST.motor(1, -1 * spinSpeed * fuckedUpMotorOffset);
      ST.motor(2, spinSpeed);
      
    }

	if(!isDigit(inByte))
	{
		return;
	}	
	int command = inByte - '0';
	int leftSignal;
	int rightSignal;
	int leftDiff;
	int rightDiff;

	if(inByte == '0')
	{
      Serial.print("stop motor");
      ST.motor(1, 0);
      ST.motor(2, 0);
	}
	else
	{
		leftDiff = command - middleSignal;
		rightDiff = -1 * leftDiff;
		if(leftDiff < 0)
		{
			leftDiff = 0;
		}
		if(rightDiff < 0)
		{
			rightDiff = 0;
		}

		leftSignal = int((neutral + ((gradientRange - rightDiff) * motorGradient)) * fuckedUpMotorOffset);
		rightSignal = neutral + ((gradientRange - leftDiff) * motorGradient);

		ST.motor(1, leftSignal);
    ST.motor(2, rightSignal);
    //Serial.printf("M1: %s, | M2: %s", leftSignal, rightSignal);  
    Serial.print("M1: ");
    Serial.print(leftSignal);
    Serial.print("  | M2: ");
    Serial.print(rightSignal);
    Serial.print("\n"); 
	}
    
  }
  

  
  delay(100); // delay for 1/10 of a second
}

