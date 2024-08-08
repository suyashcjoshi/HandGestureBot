#include <Servo.h>

Servo myservo;

void setup() {
  myservo.attach(8);  // Attach the servo to pin 8
  Serial.begin(115200);
  Serial.println("Servo motor ready");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int servoPosition = input.toInt();
    
    if (servoPosition >= 0 && servoPosition <= 180) {
      myservo.write(30);
      Serial.print("Moved to position: ");
      Serial.println(servoPosition);
    } else {
      Serial.print("Invalid position: ");
      Serial.println(servoPosition);
    }
  }
}
