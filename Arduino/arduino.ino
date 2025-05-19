#include <Stepper.h>

// Constantes
const int STEPS_PER_REV = 2048; // Passos para uma volta completa
const float DEGREE_STEPS = (STEPS_PER_REV / 360.0f) * -1; // Passos por grau (sentido anti-horário)
const int MOTOR_SPEED = 15;

// Enum para facilitar identificação de cores
enum Cor { LARANJA, VERMELHO, AMARELO, AZUL, VERDE };

// Instâncias dos motores
Stepper motor1(STEPS_PER_REV, 2, 4, 3, 5);      // Motor LARANJA
Stepper motor2(STEPS_PER_REV, 28, 30, 29, 31);  // Motor VERMELHO
Stepper motor3(STEPS_PER_REV, 36, 38, 37, 39);  // Motor AMARELO
Stepper motor4(STEPS_PER_REV, 44, 46, 45, 47);  // Motor AZUL
Stepper motor5(STEPS_PER_REV, 50, 52, 51, 53);  // Motor VERDE

// Estrutura de configuração dos motores
struct MotorConfig {
  const char* nome;
  Stepper* motor;
};

MotorConfig motores[] = {
  {"LARANJA", &motor1},
  {"VERMELHO", &motor2},
  {"AMARELO", &motor3},
  {"AZUL", &motor4},
  {"VERDE", &motor5}
};

// Função para realizar o movimento do motor
void realizarMovimento(Stepper& motor, int quantidade) {
  for (int i = 0; i < quantidade; i++) {
    motor.step(DEGREE_STEPS * -155);
    delay(800);
    motor.step(DEGREE_STEPS * 155);
    delay(800);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Pronto para receber comandos no formato 'COR QUANTIDADE'.");

  for (int i = 0; i < 5; i++) {
    motores[i].motor->setSpeed(MOTOR_SPEED);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

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

    bool corValida = false;
    for (int i = 0; i < 5; i++) {
      if (cor.equalsIgnoreCase(motores[i].nome)) {
        realizarMovimento(*motores[i].motor, quantidade);
        Serial.print("Executado: ");
        Serial.print(motores[i].nome);
        Serial.print(" x ");
        Serial.println(quantidade);
        corValida = true;
        break;
      }
    }

    if (!corValida) {
      Serial.println("Cor inválida. Use LARANJA, VERMELHO, AMARELO, AZUL ou VERDE.");
    }
  }
}