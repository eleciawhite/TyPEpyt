#include <Servo.h> 
 
Servo middle, left, right, claw ;  // creates 4 "servo objects"
 
void setup() 
{ 
  Serial.begin(9600);
  Serial.println("--- l r m c and then 0-I for the 0 to 18, will be multiplied by 10");
  Serial.println();
  
  middle.attach(11);  // attaches the servo on pin 11 to the middle object
  left.attach(10);  // attaches the servo on pin 10 to the left object
  right.attach(9);  // attaches the servo on pin 9 to the right object
  claw.attach(6);  // attaches the servo on pin 6 to the claw object
} 

int convert_input_to_degrees(char in)
{
  int degrees = -1;
  if (('0' <= in) && ( in <= '9')) {
    degrees = 10*(in - '0');
  } else if (('A' <= in) && ( in <= 'I')) {
    degrees = 10*(in-'A' + 10);
  } else if (('a' <= in) && ( in <= 'i')) {
    degrees = 10*(in-'a' + 10);
  }
  return degrees;
  
}
void loop() 
{ 
  if (Serial.available() > 0)
  {
    char cmd;
    int param;
    cmd = Serial.read();
    while (0 == Serial.available()) {;} // spin
    param = convert_input_to_degrees(Serial.read());
    if (param < 0) {
          Serial.print("Parameter out of range: ");   
          Serial.println(param);                   
    } else {
      switch(cmd) {
        case 'm':
        case 'M':
          Serial.print("Middle to ");   
          Serial.println(param);             
          middle.write(param);
        break;
        case 'l':
        case 'L':
          Serial.print("Left to ");   
          Serial.println(param);             
          left.write(param);
        break;
        case 'r':
        case 'R':
          Serial.print("Right to ");   
          Serial.println(param);             
          right.write(param);
        break;
        case 'c':
        case 'C':
          Serial.print("Claw to ");   
          Serial.println(param);             
          claw.write(param);
        break;
        case 'h':
        case 'H':
          Serial.println("Home!");   
          middle.write(90); 
          left.write(90); 
          right.write(90);
          claw.write(170); 
        break;
        default:
          Serial.print("Do not recognize '");   
          Serial.print((char)cmd);   
          Serial.println("'");   
      }        
    }
  }
} 
