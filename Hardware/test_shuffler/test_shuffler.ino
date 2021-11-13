const int transistor1 = 3;
const int transistor2 = 3;

void setup() 
{
pinMode (transistor1, OUTPUT);
digitalWrite (transistor1, LOW);
}

void loop() 
{
  digitalWrite (transistor1, HIGH);
  delay(115);
  digitalWrite (transistor1, LOW);
  delay(1000);

}
