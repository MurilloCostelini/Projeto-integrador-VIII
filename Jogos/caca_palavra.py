import tkinter as tk
from tkinter import messagebox
import random
import string

class CacaPalavrasGame:
    def __init__(self, callback=None, on_close=None):
        self.callback = callback
        self.on_close = on_close
        self.root = tk.Tk()
        self.root.title("Caça-Palavras")
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_jogo)

        # Configurações iniciais
        self.tabela_size = 15
        self.palavras = ["VERMELHO", "AMARELO", "AZUL", "LARANJA", "VERDE"]
        self.tabela = []
        self.labels = []
        self.selecao = []
        self.pontuacao = 0
        self.tempo_restante = 120
        self.jogando = True
        self.palavras_encontradas = set()

        # Inicializa a interface e o jogo
        self.setup_ui()
        self.gerar_tabela()
        self.iniciar_cronometro()

        self.root.mainloop()

    def setup_ui(self):
        """Configura a interface gráfica do jogo."""
        self.frame_tabuleiro = tk.Frame(self.root)
        self.frame_tabuleiro.pack()

        for i in range(self.tabela_size):
            linha = []
            for j in range(self.tabela_size):
                btn = tk.Button(
                    self.frame_tabuleiro,
                    text="",
                    width=5,
                    height=2,
                    relief="solid",
                    font=("Helvetica", 14),
                    command=lambda x=i, y=j: self.selecionar_letra(x, y),
                )
                btn.grid(row=i, column=j)
                linha.append(btn)
            self.labels.append(linha)

        self.frame_controle = tk.Frame(self.root)
        self.frame_controle.pack(pady=10)

        self.tempo_label = tk.Label(self.frame_controle, text=f"Tempo: {self.tempo_restante}s", font=("Helvetica", 14))
        self.tempo_label.grid(row=0, column=0, padx=5)

        self.pontuacao_label = tk.Label(self.frame_controle, text=f"Pontos: {self.pontuacao}", font=("Helvetica", 14))
        self.pontuacao_label.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.frame_controle, text="Reiniciar", command=self.reiniciar_jogo, font=("Helvetica", 12))
        self.reset_button.grid(row=0, column=2, padx=5)

    def gerar_tabela(self):
        """Gera o tabuleiro preenchido com letras aleatórias e insere as palavras."""
        self.tabela = [["" for _ in range(self.tabela_size)] for _ in range(self.tabela_size)]

        for palavra in self.palavras:
            self.adicionar_palavra(palavra)

        for i in range(self.tabela_size):
            for j in range(self.tabela_size):
                if self.tabela[i][j] == "":
                    self.tabela[i][j] = random.choice(string.ascii_uppercase)

        for i in range(self.tabela_size):
            for j in range(self.tabela_size):
                self.labels[i][j].config(text=self.tabela[i][j], bg="white", state="normal")

    def adicionar_palavra(self, palavra):
        """Adiciona uma palavra ao tabuleiro em uma posição válida."""
        direcoes = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        random.shuffle(direcoes)

        for _ in range(100):
            x, y = random.randint(0, self.tabela_size - 1), random.randint(0, self.tabela_size - 1)
            for dx, dy in direcoes:
                if self.cabe_palavra(x, y, dx, dy, palavra):
                    for i, letra in enumerate(palavra):
                        self.tabela[x + i * dx][y + i * dy] = letra
                    return

    def cabe_palavra(self, x, y, dx, dy, palavra):
        """Verifica se a palavra cabe no tabuleiro sem sobreposição inválida."""
        for i, letra in enumerate(palavra):
            nx, ny = x + i * dx, y + i * dy
            if not (0 <= nx < self.tabela_size and 0 <= ny < self.tabela_size):
                return False
            if self.tabela[nx][ny] != "" and self.tabela[nx][ny] != letra:
                return False
        return True

    def selecionar_letra(self, x, y):
        """Gerencia a seleção de letras pelo jogador."""
        if not self.jogando:
            return

        btn = self.labels[x][y]
        if (x, y) not in self.selecao:
            btn.config(bg="yellow")
            self.selecao.append((x, y))
        else:
            btn.config(bg="white")
            self.selecao.remove((x, y))

        palavra_selecionada = self.get_palavra_selecionada()
        if palavra_selecionada in self.palavras and palavra_selecionada not in self.palavras_encontradas:
            self.marcar_palavra()
            self.pontuacao += 3
            self.pontuacao_label.config(text=f"Pontos: {self.pontuacao}")
            self.palavras_encontradas.add(palavra_selecionada)

            if len(self.palavras_encontradas) == len(self.palavras):
                self.finalizar_jogo()

    def get_palavra_selecionada(self):
        """Constrói a palavra a partir das letras selecionadas."""
        if len(self.selecao) < 2:
            return ""

        dx = self.selecao[1][0] - self.selecao[0][0]
        dy = self.selecao[1][1] - self.selecao[0][1]

        for i in range(1, len(self.selecao)):
            if (self.selecao[i][0] - self.selecao[i - 1][0] != dx or
                    self.selecao[i][1] - self.selecao[i - 1][1] != dy):
                return ""

        return "".join([self.tabela[x][y] for x, y in self.selecao])

    def marcar_palavra(self):
        """Marca a palavra encontrada no tabuleiro."""
        for x, y in self.selecao:
            self.labels[x][y].config(bg="green", state="disabled")
        self.selecao = []

    def fechar_jogo(self):
        """Função para tratar o fechamento da janela."""
        if self.jogando and self.callback:
            pontuacoes_palavras = {palavra: 0 for palavra in self.palavras}
            self.callback(pontuacoes_palavras)
        
        self.root.destroy()
        if self.on_close:
            self.on_close()

    def finalizar_jogo(self):
        self.jogando = False
        for linha in self.labels:
            for label in linha:
                label.config(state="disabled")

        messagebox.showinfo("Parabéns!", f"Você encontrou todas as palavras! Pontuação final: {self.pontuacao}")

        if self.callback:
            pontuacoes_palavras = {palavra: (3 if palavra in self.palavras_encontradas else 0) for palavra in self.palavras}
            self.callback(pontuacoes_palavras)

        self.root.after(1000, self.fechar_jogo)

    def iniciar_cronometro(self):
        if self.tempo_restante > 0 and self.jogando:
            self.tempo_restante -= 1
            self.tempo_label.config(text=f"Tempo: {self.tempo_restante}s")
            self.root.after(1000, self.iniciar_cronometro)
        elif self.jogando:
            self.jogando = False
            for linha in self.labels:
                for label in linha:
                    label.config(state="disabled")

            messagebox.showinfo("Fim de Jogo", f"Tempo esgotado! Pontuação final: {self.pontuacao}")
            if self.callback:
                pontuacoes_palavras = {palavra: (3 if palavra in self.palavras_encontradas else 0) for palavra in self.palavras}
                self.callback(pontuacoes_palavras)

            self.root.after(1000, self.fechar_jogo)

    def reiniciar_jogo(self):
        """Reinicia o jogo."""
        self.tempo_restante = 120
        self.pontuacao = 0
        self.palavras_encontradas.clear()
        self.pontuacao_label.config(text=f"Pontos: {self.pontuacao}")
        self.tempo_label.config(text=f"Tempo: {self.tempo_restante}s")
        self.jogando = True
        self.gerar_tabela()
        self.iniciar_cronometro()