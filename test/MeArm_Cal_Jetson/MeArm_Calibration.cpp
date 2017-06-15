// Uses https://github.com/basilfx/Arduino-CommandLine

#include <CommandLine.h>
#include <Servo.h> 
#include "configuration.h"
#include "MeArm.h"

static void handleHelp(char* tokens);
static void handleGo(char* token);
static void handleGd(char* token);
static void handleHome(char* tokens);
static void handleClaw(char* token);

// CommandLine instance.
CommandLine commandLine(Serial,(char*)"> ");
Command CmdHelp = Command((char*)"help", &handleHelp);
Command CmdHomeAll = Command((char*)"home", &handleHome);
Command CmdClawMove = Command((char*)"c", &handleClaw);

#define ARM_IK 1
#if ARM_IK
    meArm arm(
      BASE_MIN_PWM,     BASE_MAX_PWM,     BASE_MIN_ANGLE_RAD,     BASE_MAX_ANGLE_RAD,
      SHOULDER_MIN_PWM, SHOULDER_MAX_PWM, SHOULDER_MIN_ANGLE_RAD, SHOULDER_MAX_ANGLE_RAD,
      ELBOW_MIN_PWM,    ELBOW_MAX_PWM,    ELBOW_MIN_ANGLE_RAD,    ELBOW_MAX_ANGLE_RAD,
      CLAW_MIN_PWM,     CLAW_MAX_PWM,     CLAW_MIN_ANGLE_RAD,     CLAW_MAX_ANGLE_RAD);

    Command CmdGo = Command((char*)"go", handleGo);
    Command CmdGd = Command((char*)"gd", handleGd);
#else
    Servo base, shoulder, elbow, claw;  
    
    Command CmdShoulderMove = Command((char*)"s", &handleShoulder);
    Command CmdBaseMove = Command((char*)"b", &handleBase);
    Command CmdElbowMove = Command((char*)"e", &handleElbow);
#endif // ARM_IK

 
void setup() 
{ 
    Serial.begin(9600);
    Serial.println("MeArm Calibration");
    Serial.println();

    commandLine.add(CmdHelp);
    commandLine.add(CmdHomeAll);
    commandLine.add(CmdClawMove);

#if ARM_IK
   arm.begin(BASE_PIN, SHOULDER_PIN, ELBOW_PIN, CLAW_PIN);
   commandLine.add(CmdGo);
   commandLine.add(CmdGd);
#else
    base.attach(BASE_PIN);  
    shoulder.attach(SHOULDER_PIN); 
    elbow.attach(ELBOW_PIN); 
    claw.attach(CLAW_PIN);

    // Commands
    commandLine.add(CmdShoulderMove);
    commandLine.add(CmdBaseMove);
    commandLine.add(CmdElbowMove);
#endif // ARM_IK
}

void loop() 
{ 
    commandLine.update();
} 

#if ARM_IK

void handleHome(char* tokens)
{
  arm.gotoPoint(HOME_X, HOME_Y, HOME_Z);
  arm.closeGripper();
}
void handleClaw(char* token)
{
    token = strtok(NULL, " ");
    if (token != NULL) {
        int value = atoi(token);
        if (value > 0) {
            arm.openGripper();
        } else {
            arm.closeGripper();
        }
    }
}
void handleGd(char* token)
{
    token = strtok(NULL, " ");
    int x, y, z;
    if (token != NULL) {
        x = atoi(token);
        token = strtok(NULL, " ");
    }
    if (token != NULL) {
        y = atoi(token);
        token = strtok(NULL, " ");
    } 
    if (token != NULL) {
        z = atoi(token);
        arm.goDirectlyTo(x, y, z);
    } else {
          Serial.println("Go takes three parameter: x y and z. Try 0 66 180");
    }
}
void handleGo(char* token)
{
    token = strtok(NULL, " ");
    int x, y, z;
    if (token != NULL) {
        x = atoi(token);
        token = strtok(NULL, " ");
    }
    if (token != NULL) {
        y = atoi(token);
        token = strtok(NULL, " ");
    } 
    if (token != NULL) {
        z = atoi(token);
        arm.gotoPoint(x, y, z);
    } else {
          Serial.println("Go takes three parameter: x y and z. Try 0 66 180");
    }
}

#else
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
    if (getPwmValueWithLimits(token, SHOULDER_MAX_PWM, SHOULDER_MIN_PWM, &pwm)) {
        shoulder.write(pwm);
    }
}
void handleElbow(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, ELBOW_MAX_PWM, ELBOW_MIN_PWM, &pwm)) {
        elbow.write(pwm);
    }
}
void handleClaw(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, CLAW_MAX_PWM, CLAW_MIN_PWM, &pwm)) {
        claw.write(pwm);
    }
}
void handleBase(char* token)
{
    int pwm;
    if (getPwmValueWithLimits(token, BASE_MAX_PWM, BASE_MIN_PWM, &pwm)) {
        base.write(pwm);
    }
}
void handleHome(char* tokens)
{
    base.write(BASE_HOME_PWM); 
    shoulder.write(SHOULDER_HOME_PWM); 
    elbow.write(ELBOW_HOME_PWM);
    claw.write(CLAW_HOME_PWM); 
    Serial.println("Done!");   
}
#endif
static void handleHelp(char* tokens)
{
    Serial.println("No help is available at this time.");
}

