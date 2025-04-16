#include <Stepper.h>

#define STEPS_PER_REV 2048 // Passos para uma volta completa 
#define DEGREE_STEPS (STEPS_PER_REV / 360.0)*(-1) // Passos por grau * -1 Pq é anti horário

/*   QUAL PINO DO MOTOR PARA QUAL PINO DO ARDUINO:

   MOTOR 1     MOTOR 2     MOTOR 3     MOTOR 4     MOTOR 5
  IN1 >> 2 | IN1 >> 28 | IN1 >> 36 | IN1 >> 44 | IN1 >> 50 
  IN2 >> 3 | IN2 >> 29 | IN2 >> 37 | IN2 >> 45 | IN2 >> 51 
  IN3 >> 4 | IN3 >> 30 | IN3 >> 38 | IN3 >> 46 | IN3 >> 52 
  IN4 >> 5 | IN4 >> 31 | IN4 >> 39 | IN4 >> 47 | IN4 >> 53 

*/

Stepper motor1(STEPS_PER_REV, 2, 4, 3, 5); // Motor LARANJA
Stepper motor2(STEPS_PER_REV, 28, 30, 29, 31); // Motor VERMELHO
Stepper motor3(STEPS_PER_REV, 36, 38, 37, 39); // Motor AMARELO
Stepper motor4(STEPS_PER_REV, 44, 46, 45, 47); // Motor AZUL
Stepper motor5(STEPS_PER_REV, 50, 52, 51, 53); // Motor VERDE

const int MOTOR_SPEED = 15;

const int RELE_PIN = 7;

void realizarMovimento(Stepper &motor, int quantidade) {
  digitalWrite(RELE_PIN, HIGH);

  for (int i = 0; i < quantidade; i++) {
    motor.step(DEGREE_STEPS * -155);
    delay(800);
    motor.step(DEGREE_STEPS * 155);
    delay(800);
  }
  
  digitalWrite(RELE_PIN, LOW);
}

void setup() {
  motor1.setSpeed(MOTOR_SPEED);
  motor2.setSpeed(MOTOR_SPEED);
  motor3.setSpeed(MOTOR_SPEED);
  motor4.setSpeed(MOTOR_SPEED);
  motor5.setSpeed(MOTOR_SPEED);

  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, LOW);

  Serial.begin(9600);
  Serial.println("Pronto para receber comandos no formato 'COR QUANTIDADE'.");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    // Dividir comando em partes (cor e quantidade)
    int espaco = comando.indexOf(' ');
    if (espaco == -1) {
      Serial.println("Formato inválido. Use 'COR QUANTIDADE'.");
      return;
    }

    String cor = comando.substring(0, espaco);
    int quantidade = comando.substring(espaco + 1).toInt();

    if (quantidade <= 0) {
      Serial.println("Quantidade inválida. Deve ser um número maior que 0.");
      return;
    }

    // Associar cor ao motor e realizar movimento
    if (cor == "LARANJA") {
      realizarMovimento(motor1, quantidade);
    } else if (cor == "VERMELHO") {
      realizarMovimento(motor2, quantidade);
    } else if (cor == "AMARELO") {
      realizarMovimento(motor3, quantidade);
    } else if (cor == "AZUL") {
      realizarMovimento(motor4, quantidade);
    } else if (cor == "VERDE") {
      realizarMovimento(motor5, quantidade);
    } else {
      Serial.println("Cor inválida. Use LARANJA, VERMELHO, AMARELO, AZUL ou VERDE.");
      return;
    }

    Serial.println("OK");
  }
}
