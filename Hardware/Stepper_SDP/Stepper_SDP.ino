#include <Stepper.h>
// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);
void setup() {
  //max is about 10
  myStepper.setSpeed(10);
  
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
}
void loop() {
  // Step one revolution in one direction:
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(500);
}
