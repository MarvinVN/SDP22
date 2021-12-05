#include <Stepper.h>
//^^ included library
const int stepsPerRevolution = 2045; //ammount of gear turns (div by 5)
const int Dispensor = 2;  // pin for dispensot that connects to transistor
Stepper myStepper = Stepper(stepsPerRevolution, 8, 9, 10, 11); // funciton from the stepper lib

void setup() {
  pinMode (Dispensor, OUTPUT); // sets pinmode
  // max is about 10
  digitalWrite(Dispensor, LOW);
  myStepper.setSpeed(5); // 5 revs per min ~ 12s per cycle
  Serial.begin(9600);  
}
void loop() {
  // 2048 full rotation
  // Step one revolution in one direction:
    char playerRequest;
    int playerRequestInt;
    if (Serial.available() > 0) {    // is a character available?
      playerRequest = Serial.read(); // we read from the serial monitor to see if a input is there
      Serial.print(playerRequest);
      Serial.println();
      playerRequestInt = playerRequest - '0'; //gets the int of the char
      if ((playerRequestInt > 0) && (playerRequestInt < 6)){ // if within bounds of players
        myStepper.step((stepsPerRevolution/5) * (playerRequestInt - 1)); // the nuber of 2pi/5 it must rotate
        delay(1000);
        digitalWrite(Dispensor, HIGH);
        delay(515);
        digitalWrite(Dispensor, LOW);
        delay(1000);
        myStepper.step(-(stepsPerRevolution/5) * (playerRequestInt - 1)); //where it rotates back to the origin
        Serial.print("Waiting for input: ");
      } else if(playerRequestInt == 0){
          for(int y = 0; y < 2 ; y++){ // the two dispensor rotations for initial dealing
             delay(1000); 
             digitalWrite(Dispensor, HIGH); // we pulse the motor dealing one card
             delay(215);
             digitalWrite(Dispensor, LOW);
             delay(1000);
             for(int i = 0; i < 4; i++){ // the 5 segments of the circle for players
                myStepper.step(stepsPerRevolution/5); // rotate 2pi/5 the total gears over 5
                delay(1000);
                digitalWrite(Dispensor, HIGH);
                delay(215);
                digitalWrite(Dispensor, LOW);
                delay(1000);
              }
            myStepper.step(- (4 * stepsPerRevolution / 5)); // go back to the origin 
      }
      Serial.println("Waiting for input "); // waits for user input to dispense
    }
      }else {
        return;
      }  
}
