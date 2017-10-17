#include <Servo.h>

const int analogInPin = A0;	// Analog input pin that the IR sensor is attached to
Servo irservo;

int servoPos = 70;		// Servo for IRsensor, position in degrees
int servodirection = 0;		// Servo scan left 0, right 1
int servomode = 0;
int sensorValue[18];		// IR sensor read value
int srdebug,sr[10];			// 10 samples for ir sensor readings
int motorpowerl = 255;		// Default motor PWM power, motor 1
int motorpowerr = 255;		// Default motor PWM power, motor 2
int movemode = 4;

void setup() {
  Serial.begin(9600);		// Initialize serial com at 9600bps
  //irservo.attach(9); 		// Attach servo for IRsensor, pin 9
  pinMode(3, OUTPUT);		// Initialize motor drive pin, Pairs are 2&3 and 4&5
  pinMode(6, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(13, OUTPUT);
  irservo.write(70);				// Send servo to center
  delay(500);					// Servo move delay
}

void irscan() {
	int i = 0;
	for (servoPos = 0; servoPos <= 150; servoPos += 8) {	// Sweep servo loop
		irservo.write(servoPos);	// Move servo
		delay(50);			// Wait until servo has moved
		for (i = 0; i < 10; i += 1) {
			sr[i] = analogRead(analogInPin); //Read IR sensor values to array
			delay(5);
		}
		sensorValue[servoPos/8] = (sr[0]+sr[1]+sr[2]+sr[3]+sr[4]+sr[5]+sr[6]+sr[7]+sr[8]+sr[9]) / 10;	//Average IR sensor values
	}
	irservo.write(70);				// Send servo to center
	delay(200);					// Servo move delay
}

void sendserial() {
	int i = 0;
	for (i = 0; i <= 18; i += 1) {
		// Serial.print(i); //Debug line
		// Serial.print("-"); //Debug line
		Serial.println(sensorValue[i]);		// Send IR sensor values
		delay(5);				// Delay for Serial data
	}
}

void motors() {
	int i = 0, crashread = 0;
	/*crashread = analogRead(analogInPin);
	if(crashread > 350){
		if (movemode == 9 || movemode == 0 || movemode ==4) movemode=13;
	}
	if(crashread > 250){
		if (movemode == 9 || movemode == 0) {
		movemode=13;
		motorpowerl=motorpowerl/3;
		motorpowerr=motorpowerr/3;
		}
	}
	if(crashread < 200 && movemode == 13){movemode = 4;}	*/
	if(movemode==0){
		analogWrite(3, motorpowerl); 
		digitalWrite(6, 0);
		analogWrite(10, motorpowerr);
		digitalWrite(11, 0);
		delay(350);
		movemode=4; //stop after a move
	}
	if(movemode==1){
		analogWrite(3, 0); 
		analogWrite(6, motorpowerl);
		analogWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(250);
		movemode=4; //stop after a move
	}
	if(movemode==2){
		analogWrite(3, motorpowerl); 
		analogWrite(6, 0);
		analogWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(150);
		movemode=4; //stop after a move
	}
	if(movemode==3){
		analogWrite(3, 0); 
		analogWrite(6, motorpowerl);
		analogWrite(10, motorpowerr);
		analogWrite(11, 0);
		delay(150);
		movemode=4; //stop after a move
	}
	if(movemode==5){
		analogWrite(3, motorpowerl); 
		analogWrite(6, 0);
		analogWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(50);
		movemode=4; //stop after a move
	}
	if(movemode==6){
		analogWrite(3, 0); 
		analogWrite(6, motorpowerl);
		analogWrite(10, motorpowerr);
		analogWrite(11, 0);
		delay(50);
		movemode=4; //stop after a move
	}
	if(movemode==7){
		analogWrite(3, motorpowerl); 
		analogWrite(6, 0);
		analogWrite(10, motorpowerr);
		analogWrite(11, 0);
		delay(70);
		movemode=4; //stop after a move
	}
	if(movemode==8){
		analogWrite(3, 0); 
		analogWrite(6, motorpowerl);
		analogWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(70);
		movemode=4; //stop after a move
	}
	if(movemode==9){ // constant movement mode forward
		analogWrite(3, motorpowerl); 
		digitalWrite(6, 0);
		analogWrite(10, motorpowerr);
		digitalWrite(11, 0);
		delay(5);
	}
	if(movemode==10){ // constant movement mode backward
		digitalWrite(3, 0); 
		analogWrite(6, motorpowerl);
		digitalWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(5);
	}
	if(movemode==11){ // constant tank turn left
		analogWrite(3, motorpowerl); 
		digitalWrite(6, 0);
		digitalWrite(10, 0);
		analogWrite(11, motorpowerr);
		delay(5);
	}
	if(movemode==12){ // constant tank turn right
		digitalWrite(3, 0); 
		analogWrite(6, motorpowerl);
		analogWrite(10, motorpowerr);
		digitalWrite(11, 0);
		delay(5);
	}
	if(movemode==4){
		analogWrite(3, 0); 
		analogWrite(6, 0);
		analogWrite(10, 0);
		analogWrite(11, 0);
	}
	if(movemode==13){ //emergency break/reverse
		analogWrite(3, 0); 
		analogWrite(6, 80);
		analogWrite(10, 0);
		analogWrite(11, 80);
	}
}

void servos() {
	if(servomode==0){
		irservo.write(70);				// Send servo to center
		delay(200);					// Servo move delay
	}
	if(servomode==1){
		if (servodirection == 0) {
			if(servoPos > 40) {servoPos--;} else {servodirection=1;} 
			irservo.write(servoPos);				// Send servo to center
			delay(200);
		}
		if (servodirection == 1) {
			if(servoPos < 100) {servoPos++;} else {servodirection=0;} 
			irservo.write(servoPos);				// Send servo to center
			delay(200);
		}
	}
	if(servomode==2){
		irservo.write(servoPos);			// Send servo to center
	}
}

void irdebugmode() {
	char serreadchar = '\0';
	while(serreadchar != 'y') {
		srdebug = analogRead(analogInPin); //Read IR sensor values
		delay(5);
		Serial.println(srdebug);		// Send IR sensor values
		delay(5);
		if ( Serial.available() > 0 ) {
    		serreadchar = Serial.read(); // read command from Raspi
		}
  	}
}

void readserial() {
	char serreadchar = '\0';
	char serreadbyte[] = {'\0', '\0'};
	if ( Serial.available() > 0 ) {
    		serreadchar = Serial.read(); // read command from Raspi
  	}
	if ( serreadchar == 'w' ) movemode = 0; // Forwards
	if ( serreadchar == 'a' ) movemode = 2; // Left
	if ( serreadchar == 's' ) movemode = 1; // Backwards
	if ( serreadchar == 'd' ) movemode = 3; // Right
	if ( serreadchar == 'z' ) movemode = 5; // Left SMALL
	if ( serreadchar == 'c' ) movemode = 6; // Right SMALL
	if ( serreadchar == 'r' ) movemode = 7; // Front SMALL
	if ( serreadchar == 'f' ) movemode = 8; // Back SMALL
	if ( serreadchar == 'x' ) movemode = 4; // Stop (force)

	if ( serreadchar == 'n' ) {
                motorpowerl=255;
                motorpowerr=255;
	}

	if ( serreadchar == 'W' ) movemode = 9; // Forwards constant
	if ( serreadchar == 'A' ) movemode = 11; // Left constant
	if ( serreadchar == 'S' ) movemode = 10; // Backwards constant
	if ( serreadchar == 'D' ) movemode = 12; // Right constant

	if ( serreadchar == 'm' ) {
    		Serial.readBytes(serreadbyte,2); // read motor value 1
                motorpowerl=int(serreadbyte[0]);
                motorpowerr=int(serreadbyte[1]);
		Serial.println(motorpowerl); //debug
		Serial.println(motorpowerr); //debug
//		Serial.println(serreadbyte[0]); //debug
//		Serial.println(serreadbyte[1]); //debug
		delay(5);
	}

	if ( serreadchar == 't' ) irdebugmode(); // Go to IRdebugmode

	if ( serreadchar == 'o' ) {
		irservo.detach(); // servo shutdown
		}

	if ( serreadchar == 'p' ) {
		irservo.attach(9); // servo start
		}

	if ( serreadchar == 'h' ) { // servo stop middle
		servomode = 0;
		servos();
	}
	if ( serreadchar == 'j' ) { // servo slow scan left-right
		servomode = 1;
	}
	if ( serreadchar == 'k' ) { // servo move left
		servoPos--;
		servomode = 2;
		servos();
	}
	if ( serreadchar == 'l' ) { // servo move right
		servoPos++;
		servomode = 2;
		servos();
	}
	if ( serreadchar == 'g' ) {		// IR scan and send data
		irscan();
		sendserial();
	}
}

void loop() {
	//sendserial();	 // Send information via Serial connection
	readserial();
	motors();	 // Update OUT pin signals for motors	
	if(servomode == 1) servos();
}
