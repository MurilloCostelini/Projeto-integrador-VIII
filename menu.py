import tkinter as tk
from tkinter import ttk
import serial
import time
from Jogos.caca_palavra import CacaPalavrasGame
from Jogos.roleta import jogar_roleta

# Configuração da porta serial
PORTA_SERIAL = 'COM6'
BAUD_RATE = 9600

try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
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

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("Separador de M&Ms")
        self.root.configure(bg="#2e2e2e")
        
        # Configuração responsiva
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Centralizar janela e ajustar ao tamanho da tela
        window_width = 1000
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.minsize(800, 600)  # Tamanho mínimo
        
    def create_widgets(self):
        # Estilo para os widgets
        style = ttk.Style()
        style.configure('TFrame', background='#2e2e2e')
        style.configure('Gold.TLabel', 
                        foreground='#FFD700', 
                        background='#2e2e2e', 
                        font=('Helvetica', 40, 'bold'))
        style.configure('Game.TButton', 
                       foreground='white', 
                       background='#3e3e3e',
                       font=('Helvetica', 14, 'bold'),
                       padding=10)
        style.configure('Action.TButton', 
                       foreground='white', 
                       background='#5e5e5e',
                       font=('Helvetica', 18, 'bold'),
                       padding=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Separador de M&Ms",
            style='Gold.TLabel'
        )
        titulo.grid(row=0, column=0, pady=(0, 30))
        
        # Frame para os jogos
        games_frame = ttk.Frame(main_frame)
        games_frame.grid(row=1, column=0, pady=20, sticky='nsew')
        games_frame.columnconfigure(0, weight=1)
        games_frame.columnconfigure(1, weight=1)
        
        # Botões dos jogos
        botao_caca_palavras = ttk.Button(
            games_frame,
            text="Caça-Palavras",
            style='Game.TButton',
            command=self.processar_caca_palavra
        )
        botao_caca_palavras.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        
        botao_roleta = ttk.Button(
            games_frame,
            text="Roleta",
            style='Game.TButton',
            command=self.processar_roleta
        )
        botao_roleta.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')
        
        # Botão de ação
        botao_recolher = ttk.Button(
            main_frame,
            text="Recolher 6 M&Ms",
            style='Action.TButton',
            command=self.recolher_mms
        )
        botao_recolher.grid(row=2, column=0, pady=(20, 0), sticky='ew')
        
        # Configurar expansão dos elementos
        main_frame.rowconfigure(1, weight=1)
        
    def processar_caca_palavra(self):
        def receber_resultado(quantidades):
            print(f"Quantidades distribuídas Caca Palavra: \t\t{quantidades}")
            lista_quantidades = list(quantidades.values())
            enviar_comando(",".join(map(str, lista_quantidades)))
        
        # Esconder a janela principal
        self.root.withdraw()
        CacaPalavrasGame(callback=receber_resultado, on_close=self.show_main_window)
    
    def processar_roleta(self):
        def receber_resultado(quantidades):
            print(f"Quantidades distribuídas Roleta: \t\t{quantidades}")
            lista_quantidades = list(quantidades.values())
            enviar_comando(",".join(map(str, lista_quantidades)))
        
        # Esconder a janela principal
        self.root.withdraw()
        jogar_roleta(self.root, callback=receber_resultado, on_close=self.show_main_window)
    
    def recolher_mms(self):
        """Simula o comando de recolher 6 M&Ms."""
        print("Recolher 6 M&Ms")
        enviar_comando("RECOLHER")
    
    def show_main_window(self):
        """Mostra novamente a janela principal."""
        self.root.deiconify()

# Configuração da janela principal
root = tk.Tk()
app = MainApplication(root)
root.mainloop()