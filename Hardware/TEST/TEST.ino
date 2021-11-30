#include <Stepper.h>
// Define number of steps per rotation:
const int stepsPerRevolution = 2045;
const int Dispensor = 2;

Stepper myStepper = Stepper(stepsPerRevolution, 8, 9, 10, 11);
void setup() {
  pinMode (Dispensor, OUTPUT);
  // max is about 10
  myStepper.setSpeed(5);
  Serial.begin(9600);
  for(int y = 0; y < 2 ; y++){
     delay(1000);
     digitalWrite(Dispensor, HIGH);
     delay(115);
     digitalWrite(Dispensor, LOW);
     delay(1000);
     for(int i = 0; i < 4; i++){
        myStepper.step(stepsPerRevolution/5);
        delay(1000);
        digitalWrite(Dispensor, HIGH);
        delay(115);
        digitalWrite(Dispensor, LOW);
        delay(1000);
    }
    myStepper.step(-stepsPerRevolution);
  }
  Serial.print("Done Shuffling ");
  Serial.println("Waiting for input ");
}
void loop() {
  // 2048 full rotation
  // Step one revolution in one direction:
    char playerRequest;
    int playerRequestInt;
    if (Serial.available() > 0) {    // is a character available?
      playerRequest = Serial.read();
      Serial.print(playerRequest);
      Serial.println();
      playerRequestInt = playerRequest - '0';
      if ((playerRequestInt > 0) && (playerRequestInt < 6)){
        myStepper.step((stepsPerRevolution/5) * (playerRequestInt - 1));
        delay(1000);
        digitalWrite(Dispensor, HIGH);
        delay(115);
        digitalWrite(Dispensor, LOW);
        delay(1000);
        myStepper.step(-(stepsPerRevolution/5) * (playerRequestInt - 1));
        Serial.print("Waiting for input: ");
      } else {
        return;
      }
    }
}
