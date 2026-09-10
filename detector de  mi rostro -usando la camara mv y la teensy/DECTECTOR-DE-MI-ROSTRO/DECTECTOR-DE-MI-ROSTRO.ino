#define LED_VERDE 2
#define LED_ROJO  3

unsigned long ultima_lectura = 0;
const unsigned long TIMEOUT_MS = 600; // Si no hay datos en 600ms, apaga todo

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600); // Pin 0 = RX1

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
}

void loop() {
  if (Serial1.available() > 0) {
    char dato = Serial1.read();
    ultima_lectura = millis();

    if (dato == '1') {
      // Tu rostro
      digitalWrite(LED_VERDE, HIGH);
      digitalWrite(LED_ROJO, LOW);
    } 
    else if (dato == '0') {
      // Otra persona
      digitalWrite(LED_VERDE, LOW);
      digitalWrite(LED_ROJO, HIGH);
    } 
    else if (dato == 'N') {
      // No hay nadie frente al lente
      digitalWrite(LED_VERDE, LOW);
      digitalWrite(LED_ROJO, LOW);
    }
  }

  // Apagar por seguridad si la cámara deja de transmitir
  if (millis() - ultima_lectura > TIMEOUT_MS) {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_ROJO, LOW);
  }
}