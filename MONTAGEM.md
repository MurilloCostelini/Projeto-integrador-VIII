
# 🛠️ Montagem Física — Dispenser de Confeitos

Este documento descreve a montagem física e elétrica do projeto **Dispenser de Confeitos**, incluindo motores, drivers, fonte externa e controle via Arduino.

---

## 🎛️ Componentes Utilizados

- **5x Motores de passo 28BYJ-48 (bipolar)**
- **5x Drivers ULN2003**
- **1x Arduino Mega**
- **1x Fonte externa 12V (capaz de fornecer corrente suficiente para os 5 motores)**
- Fios jumpers, barra de terminais e protoboard (opcional)

---

## ⚙️ Pinos Utilizados

| Motor | Cor       | IN1 | IN2 | IN3 | IN4 |
|-------|-----------|-----|-----|-----|-----|
| M1    | LARANJA   |  2  |  3  |  4  |  5  |
| M2    | VERMELHO  | 28  | 29  | 30  | 31  |
| M3    | AMARELO   | 36  | 37  | 38  | 39  |
| M4    | AZUL      | 44  | 45  | 46  | 47  |
| M5    | VERDE     | 50  | 51  | 52  | 53  |

---

## 🔌 Alimentação

- Todos os motores são alimentados por uma **fonte externa de 12V**.
- A alimentação dos drivers ULN2003 está conectada em **paralelo**.
- Todos os **GNDs devem estar conectados entre si** (fonte, drivers e Arduino).

---

## Esquema Elétrico Resumido

Todos os motores de passo são conectados aos seus respectivos drivers (como o ULN2003), e estes drivers são alimentados por uma fonte externa de 12V. O controle de alimentação dos motores é feito pelo Arduino.

### 🧩 Conexões Gerais

``` sh
[ Fonte 12V ]
     +--------------------+--------------------+--------------------+
     |                    |                    |                    |
     |                    |                    |                    |
 [Driver M1]         [Driver M2]          [Driver M3]          [Driver M4] ...
     |                    |                    |                    |
 [Motor M1]          [Motor M2]           [Motor M3]           [Motor M4]
```

- Todos os **VCC dos drivers** são ligados em **paralelo** à saída de 12V da fonte.
- Todos os **GNDs dos drivers** e o **GND da fonte** devem estar ligados entre si e conectados também ao **GND do Arduino**.

### 🔌 Exemplo de conexão de um motor

| Ponto             | Conexão                        |
|------------------|--------------------------------|
| Motor de Passo   | Driver ULN2003                 |
| Driver IN1 a IN4 | Pinos digitais do Arduino      |
| VCC Driver       | +12V da Fonte Externa          |
| GND Driver       | GND comum (Fonte + Arduino)    |

---

## Observações Importantes

- **Todos os GNDs devem estar conectados em comum**: Arduino, drivers e fonte
- Certifique-se de que a **fonte tem corrente suficiente** para alimentar todos os motores simultaneamente.
- Organize a fiação de forma clara e segura.
- Faça testes com um motor por vez antes de ativar todos juntos.

---

## Referências

- Código do Arduino: [`arduino.ino`][internal-reference-arduino]
- Documentações de drivers ULN2003 e motores 28BYJ-48
- Datasheets dos componentes utilizados

---

Se você montar algo diferente ou tiver melhorias, envie um PR ou abra uma issue!

## **Equipe Dispenser de Confeitos — Geração SENAC**

[internal-reference-arduino]: arduino/arduino.ino