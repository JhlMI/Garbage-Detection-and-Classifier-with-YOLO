#include <Servo.h>


// Servo 1 15 - 180  Servo final 
// Servo 2 75 - 140  Servo 3
// Servo 3 0 - 90 Servo 2 
// Servo 4 0 - 90 Servo 1
Servo Ser1;
Servo Ser2;
Servo Ser3;
Servo Ser4;
void setup() {
  Serial.begin(9600);
  Ser1.attach(2);
  Ser2.attach(3);
  Ser3.attach(4);
  Ser4.attach(5);

  Ser1.write(15); // Metal - Plastic
  Ser2.write(75); // Glass
  Ser3.write(0); // Cardboard
  Ser4.write(0); // Papper 
}

void loop() {

     Ser1.write(15);
    

 if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');

    if (comando == "open_glass") {
      Ser4.write(90);  // Abrir
      delay(500);
      Ser4.write(0);   // Cerrar

    } else if (comando == "open_paper") {
      Ser3.write(90);
      delay(1200);
      Ser3.write(0);

    } else if (comando == "open_cardboard") {
      Ser2.write(140);
      delay(1500);
      Ser2.write(75);

    } else if (comando == "open_metal") {

      Ser1.write(15);
      delay(500);
      Ser1.write(180);


    } else if (comando == "open_plastic") {
      Ser1.write(180);
      delay(500);
      Ser1.write(15);

    }
  }
}
  



