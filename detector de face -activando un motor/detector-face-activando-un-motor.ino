// Pines de control del Driver
const int pinIN1 = 2;
const int pinIN2 = 4;
const int ledPlaca = 13;

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600); // Lee datos por Pin 0 (RX1)

  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);
  pinMode(ledPlaca, OUTPUT);

  apagarMotor();
}

void loop() {
  if (Serial1.available() > 0) {
    char c = Serial1.read();

    if (c == '1') {
      // Tu rostro reconocido: arranca motor y prende LED
      digitalWrite(ledPlaca, HIGH);
      digitalWrite(pinIN1, HIGH);
      digitalWrite(pinIN2, LOW);
    } 
    else if (c == '0' || c == 'N') {
      // Otra persona o nadie: frena y apaga LED
      apagarMotor();
    }
  }
}

void apagarMotor() {
  digitalWrite(ledPlaca, LOW);
  digitalWrite(pinIN1, LOW);
  digitalWrite(pinIN2, LOW);
}