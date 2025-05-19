# 🎯 Dispenser de Confeitos — Geração SENAC

Este projeto une eletrônica embarcada com interface gráfica interativa para demonstrar, de forma divertida, conceitos de programação, automação e comunicação entre sistemas. Criado por estudantes de **Engenharia da Computação** no **Centro Universitário SENAC**, ele será exibido na feira **Geração SENAC**.

## 📌 Descrição

O Dispenser de Confeitos combina um programa em Python com um microcontrolador Arduino. A interface gráfica oferece duas opções de jogo:

- 🎡 **Roleta dos Confeitos** — Gira uma roleta para determinar quantos confeitos de cada cor devem ser separados.
- 🧠 **Caça-Palavras** — Um desafio de lógica e observação onde o jogador encontra nomes de cores escondidas na matriz de letras.

Ao final de cada rodada, os dados são enviados via **serial** ao Arduino, que aciona dispositivos para realizar a separação dos confeitos.

---

## 🧠 Tecnologias Utilizadas

| Parte             | Tecnologia              |
|------------------|-------------------------|
| Interface gráfica| Python + Tkinter        |
| Comunicação      | Porta Serial (pyserial) |
| Firmware         | Arduino (.ino)          |
| Hardware         | Microcontrolador + atuadores |

---

## 🧩 Funcionalidades

### 🎡 Roleta de Confeitos

- Roleta visual gira com animação suave.
- Número sorteado é dividido entre 5 cores de confeitos.
- Comando é enviado ao Arduino para realizar a separação.

### 🧠 Caça-Palavras

- Palavras: `VERMELHO`, `AZUL`, `AMARELO`, `VERDE`, `LARANJA`.
- Temporizador de 2 minutos.
- Pontuação por palavra correta.
- Comando final com pontuação é enviado ao Arduino.

---

## 🛠️ Como Reproduzir

👉 Para detalhes da montagem elétrica, consulte [montagem.md][internal-montagem-md]

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/dispenser-confeitos.git
cd dispenser-confeitos
```

#### Navegue para a versão desejada

```bash
git checkout v1.0
```

### 2. Instalar dependências Python

Use Python 3.9 ou superior.

```bash
pip install pyserial
```

> Tkinter já vem incluso na maioria das instalações do Python. Se necessário:
>
> - Windows: já incluso
> - Linux (Debian/Ubuntu): `sudo apt install python3-tk`

### 3. Conectar o Arduino

- Conecte o Arduino via USB.
- Altere a porta serial no início do `main.py`:

  ```python
  PORTA_SERIAL = 'COM6'  # ou /dev/ttyUSB0 no Linux
  ```

### 4. Rodar a Interface

```bash
python interface/main.py
```

---

## 🔧 Upload do Código no Arduino

1. Abra o arquivo `arduino/arduino.ino` no **Arduino IDE**.
2. Selecione a placa correta (ex: Arduino Uno).
3. Faça o upload para a placa.

---

## 🎓 Sobre o Projeto

Desenvolvido como uma forma criativa de apresentar **Engenharia da Computação** a estudantes do ensino médio, o Dispenser de Confeitos demonstra:

- Comunicação Serial
- Interfaces gráficas
- Controle de hardware com software
- Pensamento lógico e gamificação

---

## 🧑‍🎓 Autores

- **Enzo Henrique Malavazi Lins**
- **Felipe Fernandes Mandelli**
- **Gabriela Carneiro Sales**
- **Gregorio Alves Rodrigues da Cruz**
- **Murillo Tiberio Costelini**
- **Saymon Jesus Souza**
- **Thiago de Andrade Silva**

Estudantes de Engenharia da Computação — Centro Universitário SENAC  
Expositores na Feira Geração SENAC

[internal-montagem-md]: montagem.md
