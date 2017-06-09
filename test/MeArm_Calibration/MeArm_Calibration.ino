// Uses https://github.com/basilfx/Arduino-CommandLine

#include <CommandLine.h>
#include <Servo.h> 

#define SHOULDER_MAX 160
#define SHOULDER_MIN 60
#define SHOULDER_HOME 90
#define ELBOW_MAX 180
#define ELBOW_MIN 20
#define ELBOW_HOME 90
#define CLAW_MAX 180
#define CLAW_MIN 0
#define CLAW_HOME 170
#define BASE_MAX 180
#define BASE_MIN 0
#define BASE_HOME 90

Servo base, shoulder, elbow, claw ;  

// CommandLine instance.
CommandLine commandLine(Serial, "> ");

Command CmdHelp = Command("help", &handleHelp);
Command CmdShoulderMove = Command("s", &handleShoulder);
Command CmdBaseMove = Command("b", &handleBase);
Command CmdElbowMove = Command("e", &handleElbow);
Command CmdClawMove = Command("c", &handleClaw);
Command CmdHomeAll = Command("home", &handleHome);
 
void setup() 
{ 
    Serial.begin(9600);
    Serial.println("MeArm Calibration");
    Serial.println();

    base.attach(11);  // attaches the servo on pin 11 to the base object
    shoulder.attach(10);  // attaches the servo on pin 10 to the shoulder object
    elbow.attach(9);  // attaches the servo on pin 9 to the elbow object
    claw.attach(6);  // attaches the servo on pin 6 to the claw object

    // Commands
    commandLine.add(CmdHelp);
    commandLine.add(CmdShoulderMove);
    commandLine.add(CmdBaseMove);
    commandLine.add(CmdElbowMove);
    commandLine.add(CmdClawMove);
    commandLine.add(CmdHomeAll);
}

void loop() 
{ 
    commandLine.update();
} 

bool getPwmValueWithLimits(char *str, int max, int min, int *value_out)
{
    bool goodValue = false;
    int value;
    char* token = strtok(NULL, " ");
    if (token != NULL) {
        int value = atoi(token);
        if (( max >= value)  && (value >= min)){
            *value_out = value;
            goodValue = true;
        } else {
            Serial.print("Value outside range for this servo: ");
            Serial.print(min);
            Serial.print(" and ");
            Serial.println(max);
        }
    } else {
        Serial.println("Need pwm value!");
    }
    return goodValue;
}

void handleShoulder(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, SHOULDER_MAX, SHOULDER_MIN, &pwm)) {
        shoulder.write(pwm);
    }
}
void handleElbow(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, ELBOW_MAX, ELBOW_MIN, &pwm)) {
        elbow.write(pwm);
    }
}
void handleClaw(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, CLAW_MAX, CLAW_MIN, &pwm)) {
        claw.write(pwm);
    }
}
void handleBase(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, BASE_MAX, BASE_MIN, &pwm)) {
        base.write(pwm);
    }
}
void handleHome(char* tokens)
{
    base.write(BASE_HOME); 
    shoulder.write(SHOULDER_HOME); 
    elbow.write(ELBOW_HOME);
    claw.write(CLAW_HOME); 
    Serial.println("Done!");   
}

void handleHelp(char* tokens)
{
    Serial.println("No help is available at this time.");
}
