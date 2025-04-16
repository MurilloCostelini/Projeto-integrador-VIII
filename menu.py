import tkinter as tk
import subprocess
import serial
import time
from Jogos.caca_palavra import CacaPalavrasGame
from Jogos.roleta import jogar_roleta

# Configuração da porta serial (ajuste conforme necessário)
PORTA_SERIAL = 'COM6'  # Substitua pela porta correta do Arduino
BAUD_RATE = 9600

try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)  # Aguarda inicialização da porta serial
    print("Conexão com o Arduino estabelecida!")
except Exception as e:
    print(f"Erro ao conectar na porta serial: {e}")
    arduino = None

def enviar_comando(comando):
    """Envia um comando para o Arduino via porta serial."""
    print(f"Enviando comando arduino: {comando}")
    if arduino:
        try:
            arduino.write(f"{comando}\n".encode())
            print(f"Comando enviado ao Arduino: {comando}")
        except Exception as e:
            print(f"Erro ao enviar comando: {e}")
    else:
        print("Erro: Arduino não conectado.")


def processar_caca_palavra():
    def receber_resultado(quantidades):
        print(f"Quantidades distribuídas Caca Palavra: \t\t{quantidades}")
        lista_quantidades = list(quantidades.values())  # Converte o dict em uma lista
        enviar_comando(",".join(map(str, lista_quantidades)))  # Envia ao Arduino

    CacaPalavrasGame(callback=receber_resultado)

def processar_roleta():
    def receber_resultado(quantidades):
        print(f"Quantidades distribuídas Roleta: \t\t{quantidades}")
        lista_quantidades = list(quantidades.values())  # Converte o dict em uma lista
        enviar_comando(",".join(map(str, lista_quantidades)))  # Envia ao Arduino

    jogar_roleta(root, callback=receber_resultado)

def recolher_mms():
    """Simula o comando de recolher 6 M&Ms."""
    print("Recolher 6 M&Ms")
    enviar_comando("RECOLHER")

# Configuração da janela principal
root = tk.Tk()
root.title("Separador de M&Ms")
root.geometry("1080x1080")
root.configure(bg="#2e2e2e")  # Fundo cinza escuro (modo noturno)

# Título
titulo = tk.Label(
    root,
    text="Separador de M&Ms",
    font=("Helvetica", 40, "bold"),
    fg="#FFD700",  # Cor dourada
    bg="#2e2e2e",
)
titulo.pack(pady=30)

# Frame para os botões dos jogos
frame_jogos = tk.Frame(root, bg="#2e2e2e")
frame_jogos.pack(expand=True)

# Função para criar botões
def criar_botao(frame, text, command):
    botao = tk.Button(
        frame,
        text=text,
        font=("Helvetica", 14, "bold"),
        fg="white",
        bg="#3e3e3e",
        width=20,
        height=5,
        command=command,
    )
    return botao


# Botões dos jogos
botao_caca_palavras = criar_botao(
    frame_jogos,
    "Caça-Palavras",
    lambda: processar_caca_palavra()
)

botao_roleta = criar_botao(
    frame_jogos,
    "Roleta",
    lambda: processar_roleta()
)

# Organizar os botões em grade
botao_caca_palavras.grid(row=0, column=0, padx=20, pady=20)
botao_roleta.grid(row=0, column=1, padx=20, pady=20)

# Botão para "Recolher 6 M&Ms"
botao_recolher = tk.Button(
    root,
    text="Recolher 6 M&Ms",
    font=("Helvetica", 18, "bold"),
    fg="white",
    bg="#5e5e5e",
    width=20,
    height=2,
    command=recolher_mms,
)
botao_recolher.pack(pady=20)

# Executa a janela principal
root.mainloop()
