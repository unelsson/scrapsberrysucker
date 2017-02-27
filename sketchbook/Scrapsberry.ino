#include <Servo.h>

const int analogInPin = A0;	// Analog input pin that the IR sensor is attached to
Servo irservo;

int servoPos = 0;		// Servo for IRsensor, position in degrees
int sensorValue[18];		// IR sensor read value
int movemode = 4;

void setup() {
  Serial.begin(9600);		// Initialize serial com at 9600bps
  irservo.attach(9); 		// Attach servo for IRsensor, pin 9
  pinMode(3, OUTPUT);		// Initialize motor drive pin, Pairs are 2&3 and 4&5
  pinMode(6, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(13, OUTPUT);
}

void irscan() {
	for (servoPos = 0; servoPos <= 180; servoPos += 10) {	// Sweep servo loop
		irservo.write(servoPos);	// Move servo
		delay(20);			// Wait until servo has moved

		sensorValue[servoPos/10] = analogRead(analogInPin);	// Read IR sensor value

	}
	irservo.write(0);				// Send servo to left
	delay(100);					// Servo move delay
}

void sendserial() {
	int i = 0;
	for (i = 0; i <= 18; i += 1) {
		Serial.println(sensorValue[i]);
		delay(2);				// Delay for Serial data
	}
		Serial.println("END OF DATA");
}

void readserial() {
	char serreadchar = '\0';
	if ( Serial.available() > 0 ) {
    		serreadchar = Serial.read();
		Serial.println(serreadchar); //debug info
  	}
	if ( serreadchar == 'w' ) movemode = 0;
	if ( serreadchar == 'a' ) movemode = 2;
	if ( serreadchar == 's' ) movemode = 1;
	if ( serreadchar == 'd' ) movemode = 3;
	if ( serreadchar == 'x' ) movemode = 4;
}

void motors() {
	if(movemode==0){
		analogWrite(3, 255); 
		analogWrite(6, 0);
		analogWrite(10, 255);
		analogWrite(11, 0);
		irscan();
	}
	if(movemode==1){
		analogWrite(3, 0); 
		analogWrite(6, 150);
		analogWrite(10, 0);
		analogWrite(11, 150);
	}
	if(movemode==2){
		analogWrite(3, 255); 
		analogWrite(6, 0);
		analogWrite(10, 0);
		analogWrite(11, 0);
	}
	if(movemode==3){
		analogWrite(3, 0); 
		analogWrite(6, 0);
		analogWrite(10, 255);
		analogWrite(11, 0);
	}
	if(movemode==4){
		analogWrite(3, 0); 
		analogWrite(6, 0);
		analogWrite(10, 0);
		analogWrite(11, 0);
	}
	delay(500);
	movemode=4;
}

void loop() {
	//sendserial();	 // Send information via Serial connection
	readserial();
	//irscan();	 // Do a full IR sweep
	motors();	 // Update OUT pin signals for motors	

	//Blink leds for debug
	digitalWrite(13, HIGH);
	delay(250);
	digitalWrite(13, LOW);
	delay(250);
	digitalWrite(13, HIGH);
	delay(250);
	digitalWrite(13, LOW);
	delay(250);
}
