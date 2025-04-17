# Coisas para arrumar: 

# - Ocultar caca palavra antes de iniciar o jogo
# - Bloquear o "voltar" enquanto jogo esta ativo
# - Adicionar Embaralhar durante partida
# - Tirar caixas de notificação do resultado e mostrar na tela (*"BONITINHO"*)
# - Implementar envio para o arduino
# - Sobreposição de letra no caca palavra
# - LOGO SENAC?


import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import string
import os

# Cores oficiais do SENAC conforme o manual
AZUL_SENAC = "#004A8D"       # Azul institucional (Pantone 288 C)
LARANJA_SENAC = "#F7941D"    # Laranja institucional (Pantone 144 C)
LARANJA_CLARO = "#FDC180"    # Laranja claro (Pantone 144 em 55%)

# Configurações de cores para a aplicação
fundo = "white"        # Fundo principal (10% de saturação conforme manual)
fundo_botao_menu = LARANJA_CLARO   # Fundo dos botões
letra_titulo_menu = AZUL_SENAC
letra_botao_menu = AZUL_SENAC
fundo_roleta = "white"       # Fundo do canvas da roleta
letra_dados_caca_palavra = AZUL_SENAC
selecao_letra_caca_palavra = "sandy brown" # "tan" "burlywood" "wheat" "peru" "sandy brown"

# Variável para ajuste do padding do canvas da roleta
PADDING_CANVAS_ROLETA = 100  # Valor padrão, pode ser ajustado

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.frames = {}
        self.shared_data = {
            'pontuacao': 0,
            'configuracoes': {}
        }
        
        # Criar todos os frames
        for F in (MenuFrame, RoletaFrame, CacaPalavrasFrame):
            frame = F(self.root, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("MenuFrame")
    
    def setup_window(self):
        self.root.title("Separador de M&Ms - SENAC")
        self.root.configure(bg=fundo)

        # Configuração responsiva
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Fullscreen com opção de sair com ESC
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.minsize(800, 600)
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")
    
    def get_shared_data(self):
        return self.shared_data

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=fundo)
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal com padding maior
        main_frame = tk.Frame(self, bg=fundo)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título com fonte Helvetica conforme manual
        titulo = tk.Label(
            main_frame,
            text="Separador de M&Ms",
            font=("Helvetica", 48, "bold"),  # Helvetica Neue conforme manual
            fg=letra_titulo_menu,
            bg=fundo
        )
        titulo.pack(pady=40)
        
        # Frame para os botões com espaçamento
        buttons_frame = tk.Frame(main_frame, bg=fundo)
        buttons_frame.pack(expand=True)
        
        # Botões com estilo SENAC
        btn_roleta = ttk.Button(
            buttons_frame,
            text="Roleta",
            style='Game.TButton',
            command=lambda: self.controller.show_frame("RoletaFrame")
        )
        btn_roleta.pack(pady=20, ipadx=30, ipady=15)
        
        btn_caca = ttk.Button(
            buttons_frame,
            text="Caça-Palavras",
            style='Game.TButton',
            command=lambda: self.controller.show_frame("CacaPalavrasFrame")
        )
        btn_caca.pack(pady=20, ipadx=30, ipady=15)
        
        # Botão de saída
        btn_sair = ttk.Button(
            main_frame,
            text="Sair",
            style='Action.TButton',
            command=self.controller.root.quit
        )
        btn_sair.pack(pady=40, ipadx=20, ipady=10)

class RoletaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.callback = None
        self.setup_ui()
        self.jogando = False
    
    def voltar_se_permitido(self):
        if not self.jogando:
            self.controller.show_frame("MenuFrame")
            
    def setup_ui(self):
        self.configure(bg=fundo)
        
        # Frame principal com padding ajustável
        main_frame = tk.Frame(self, bg=fundo)
        main_frame.pack(expand=True, fill="both", padx=PADDING_CANVAS_ROLETA, pady=20)
        
        # Botão de voltar com estilo SENAC
        btn_voltar = ttk.Button(
            main_frame,
            text="Voltar ao Menu",
            style='Action.TButton',
            command= self.voltar_se_permitido
        )
        btn_voltar.pack(pady=20, anchor="nw")
        
        # Canvas para a roleta com fundo branco
        self.canvas = tk.Canvas(main_frame, width=600, height=600, bg=fundo_roleta, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Configuração dos setores com cores mais suaves
        self.setores = 20
        self.angulo_por_setor = 360 / self.setores
        self.cores = [LARANJA_CLARO, "#FFD699", "#FFE6C2", "#FFF2E0"] * (self.setores // 4)
        self.setores_embaralhados = list(range(1, 21))
        random.shuffle(self.setores_embaralhados)
        
        self.desenhar_roleta()
        self.atualiza_seta(0)
        
        # Botão para girar com estilo SENAC
        self.btn_girar = ttk.Button(
            main_frame,
            text="Girar Roleta",
            style='Game.TButton',
            command=self.girar_seta
        )
        self.btn_girar.pack(pady=20)
    
    def desenhar_roleta(self):
        for i in range(self.setores):
            angulo_inicio = i * self.angulo_por_setor
            self.canvas.create_arc(
                50, 50, 550, 550,
                start=angulo_inicio, extent=self.angulo_por_setor,
                fill=self.cores[i], outline=AZUL_SENAC, width=2  # Contorno azul SENAC
            )
            angulo_medio = math.radians(angulo_inicio + self.angulo_por_setor / 2)
            texto_x = 300 + 220 * math.cos(angulo_medio)
            texto_y = 300 - 220 * math.sin(angulo_medio)
            self.canvas.create_text(
                texto_x, texto_y, 
                text=str(self.setores_embaralhados[i]),
                font=("Helvetica", 12, "bold"), 
                fill=AZUL_SENAC  # Texto em azul SENAC
            )
    
    def atualiza_seta(self, angulo_atual):
        self.canvas.delete("seta")
        angulo_radianos = math.radians(angulo_atual)
        ponta_x = 300 + 250 * math.cos(angulo_radianos)
        ponta_y = 300 - 250 * math.sin(angulo_radianos)
        base1_x = 300 + 280 * math.cos(angulo_radianos + math.radians(10))
        base1_y = 300 - 280 * math.sin(angulo_radianos + math.radians(10))
        base2_x = 300 + 280 * math.cos(angulo_radianos - math.radians(10))
        base2_y = 300 - 280 * math.sin(angulo_radianos - math.radians(10))
        self.canvas.create_polygon(
            ponta_x, ponta_y, base1_x, base1_y, base2_x, base2_y,
            fill=LARANJA_SENAC, outline=AZUL_SENAC, width=2, tags="seta"  # Seta laranja SENAC
        )
    
    def girar_seta(self):
        self.btn_girar.config(state="disabled")
        self.jogando = True
        
        duracao_total = 3000  # 3 segundos
        passos_totais = 300
        voltas = 8
        
        numero_vencedor = random.choices(range(1, 21), k=1)[0]
        setor_vencedor = self.setores_embaralhados.index(numero_vencedor)
        angulo_final = setor_vencedor * self.angulo_por_setor + self.angulo_por_setor / 2
        angulo_final += random.uniform(-5, 5)
        angulo_total = voltas * 360 + angulo_final
        
        passo_atual = 0
        
        def animar_giro():
            nonlocal passo_atual
            if passo_atual <= passos_totais:
                angulo_atual = (angulo_total / passos_totais) * passo_atual
                intervalo = max(10, int(duracao_total / passos_totais * (1 + passo_atual / passos_totais)))
                self.atualiza_seta(angulo_atual)
                self.update()
                self.after(intervalo, animar_giro)
                passo_atual += 1
            else:
                quantidades = self.gerar_comando(numero_vencedor)
                self.exibir_resultado(quantidades, numero_vencedor)
                self.btn_girar.config(state="normal")
                self.jogando = False
        
        animar_giro()
    
    def gerar_comando(self, numero_total):
        cores_retorno = ["VERMELHO", "AMARELO", "AZUL", "LARANJA", "VERDE"]
        base = numero_total // 5
        restante = numero_total % 5
        resultado = {cor: base for cor in cores_retorno}
        for i in range(restante):
            resultado[cores_retorno[i]] += 1
        return resultado
    
    def exibir_resultado(self, quantidades, numero_vencedor):
        resultado_texto = f"Resultado da Roleta:\nNúmero vencedor: {numero_vencedor}\n"
        resultado_texto += "Quantidades de M&Ms para cada cor:\n"
        for cor, qtd in quantidades.items():
            resultado_texto += f"{cor}: {qtd}\n"
        
        messagebox.showinfo("Resultado", resultado_texto)
        
        # Se houver callback, chamar com os resultados
        if self.callback:
            self.callback(quantidades)

class CacaPalavrasFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.callback = None
        self.jogando = False  # Inicialmente não está jogando
        self.setup_ui()
    
    def setup_ui(self):
        self.configure(bg=fundo)
        
        # Frame principal
        main_frame = tk.Frame(self, bg=fundo)
        main_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Botão de voltar
        btn_voltar = ttk.Button(
            main_frame,
            text="Voltar ao Menu",
            style='Action.TButton',
            command=lambda: self.controller.show_frame("MenuFrame")
        )
        btn_voltar.pack(pady=20, anchor="nw")
        
        # Configurações do jogo
        self.tabela_size = 15
        self.palavras = ["VERMELHO", "AMARELO", "AZUL", "LARANJA", "VERDE"]
        self.tabela = []
        self.labels = []
        self.selecao = []
        self.pontuacao = 0
        self.tempo_restante = 120
        self.palavras_encontradas = set()
        
        # Frame do tabuleiro
        self.frame_tabuleiro = tk.Frame(main_frame, bg=fundo)
        self.frame_tabuleiro.pack(pady=20)
        
        # Frame de controle
        self.frame_controle = tk.Frame(main_frame, bg=fundo)
        self.frame_controle.pack(pady=20)
        
        # Labels de informação
        self.tempo_label = tk.Label(
            self.frame_controle,
            text=f"Tempo: {self.tempo_restante}s",
            font=("Helvetica", 16, "bold"),
            fg=letra_dados_caca_palavra,
            bg=fundo
        )
        self.tempo_label.grid(row=0, column=0, padx=20)
        
        self.pontuacao_label = tk.Label(
            self.frame_controle,
            text=f"Pontos: {self.pontuacao}",
            font=("Helvetica", 16, "bold"),
            fg=letra_dados_caca_palavra,
            bg=fundo
        )
        self.pontuacao_label.grid(row=0, column=1, padx=20)
        
        # Botão de iniciar/reiniciar
        self.btn_iniciar = ttk.Button(
            self.frame_controle,
            text="Iniciar Jogo",
            style='Game.TButton',
            command=self.iniciar_jogo 
        )
        self.btn_iniciar.grid(row=0, column=2, padx=20)
        
        # Cria o tabuleiro mas não inicia o jogo ainda
        self.criar_tabuleiro()

        self.frame_tabuleiro.pack_forget()

    def criar_tabuleiro(self):
        # Inicializa tabela vazia
        self.tabela = [["" for _ in range(self.tabela_size)] for _ in range(self.tabela_size)]
        
        # Adiciona palavras
        for palavra in self.palavras:
            self.adicionar_palavra(palavra)
        
        # Preenche espaços vazios com letras aleatórias
        for i in range(self.tabela_size):
            for j in range(self.tabela_size):
                if self.tabela[i][j] == "":
                    self.tabela[i][j] = random.choice(string.ascii_uppercase)
        
        # Cria os botões do tabuleiro
        for i in range(self.tabela_size):
            linha = []
            for j in range(self.tabela_size):
                btn = tk.Button(
                    self.frame_tabuleiro,
                    text=self.tabela[i][j],
                    width=3,
                    height=1,
                    font=("Helvetica", 12),
                    relief="solid",
                    command=lambda x=i, y=j: self.selecionar_letra(x, y)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                linha.append(btn)
            self.labels.append(linha)
    
    def adicionar_palavra(self, palavra):
        direcoes = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        random.shuffle(direcoes)
        
        for _ in range(100):  # Tenta 100 vezes colocar a palavra
            x, y = random.randint(0, self.tabela_size-len(palavra)), random.randint(0, self.tabela_size-len(palavra))
            for dx, dy in direcoes:
                if self.verificar_posicao(x, y, dx, dy, palavra):
                    for i, letra in enumerate(palavra):
                        self.tabela[x + i*dx][y + i*dy] = letra
                    return
    
    def verificar_posicao(self, x, y, dx, dy, palavra):
        for i, letra in enumerate(palavra):
            nx, ny = x + i*dx, y + i*dy
            if not (0 <= nx < self.tabela_size and 0 <= ny < self.tabela_size):
                return False
            if self.tabela[nx][ny] != "" and self.tabela[nx][ny] != letra:
                return False
        return True
    
    def selecionar_letra(self, x, y):
        if not self.jogando:
            return
            
        btn = self.labels[x][y]
        if (x, y) in self.selecao:
            btn.config(bg="white")
            self.selecao.remove((x, y))
        else:
            btn.config(bg=selecao_letra_caca_palavra)
            self.selecao.append((x, y))
        
        palavra = self.verificar_palavra()
        if palavra in self.palavras and palavra not in self.palavras_encontradas:
            self.marcar_palavra(palavra)
            self.pontuacao += 3
            self.pontuacao_label.config(text=f"Pontos: {self.pontuacao}")
            self.palavras_encontradas.add(palavra)
            
            if len(self.palavras_encontradas) == len(self.palavras):
                self.finalizar_jogo(vencedor=True)
    
    def verificar_palavra(self):
        if len(self.selecao) < 2:
            return ""
            
        dx = self.selecao[1][0] - self.selecao[0][0]
        dy = self.selecao[1][1] - self.selecao[0][1]
        
        for i in range(1, len(self.selecao)):
            if (self.selecao[i][0] - self.selecao[i-1][0] != dx or 
                self.selecao[i][1] - self.selecao[i-1][1] != dy):
                return ""
                
        return "".join(self.tabela[x][y] for x, y in self.selecao)
    
    def marcar_palavra(self, palavra):
        if palavra == "VERMELHO": cor = "red"
        if palavra == "VERDE": cor = "green"
        if palavra == "AMARELO": cor = "yellow"
        if palavra == "AZUL": cor = "blue"
        if palavra == "LARANJA": cor = "orange"


        for x, y in self.selecao:
            self.labels[x][y].config(bg=cor, state="disabled")
        self.selecao = []
    
    def iniciar_cronometro(self):
        if self.tempo_restante > 0 and self.jogando:
            self.tempo_restante -= 1
            self.tempo_label.config(text=f"Tempo: {self.tempo_restante}s")
            self.after(1000, self.iniciar_cronometro)
        elif self.jogando:
            self.finalizar_jogo(vencedor=False)
    
    def finalizar_jogo(self, vencedor):
        self.jogando = False
        
        for linha in self.labels:
            for btn in linha:
                btn.config(state="disabled")
        
        if vencedor:
            mensagem = f"Parabéns! Você encontrou todas as palavras!\nPontuação: {self.pontuacao}"
        else:
            mensagem = f"Tempo esgotado!\nPalavras encontradas: {len(self.palavras_encontradas)}/{len(self.palavras)}\nPontuação: {self.pontuacao}"
        
        messagebox.showinfo("Fim do Jogo", mensagem)
        
        # Se houver callback, chamar com os resultados
        if self.callback:
            resultado = {palavra: 3 if palavra in self.palavras_encontradas else 0 
                        for palavra in self.palavras}

    def iniciar_jogo(self):
        """Inicia o jogo quando o botão é clicado"""
        if not self.jogando:
            self.jogando = True
            self.palavras_encontradas = set()
            self.pontuacao = 0
            self.tempo_restante = 120
            self.pontuacao_label.config(text=f"Pontos: {self.pontuacao}")
            self.tempo_label.config(text=f"Tempo: {self.tempo_restante}s")
            self.btn_iniciar.config(text="Reiniciar")

            for linha in self.labels:
                for btn in linha:
                    btn.destroy()
            self.labels = []
            
            # Recria o tabuleiro
            self.criar_tabuleiro()
            
            # Habilita todos os botões do tabuleiro
            for linha in self.labels:
                for btn in linha:
                    btn.config(state="normal", bg="white")
            
            self.frame_tabuleiro.pack(pady=20)

            self.iniciar_cronometro()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configurar estilos conforme manual do SENAC
    style = ttk.Style()
    
    # Estilo para botões de jogo
    style.configure('Game.TButton', 
                  foreground=letra_botao_menu, 
                  background=fundo_botao_menu,
                  font=('Helvetica', 16, 'bold'),  # Helvetica conforme manual
                  padding=15,
                  borderwidth=2,
                  relief="solid")
    
    # Estilo para botões de ação
    style.configure('Action.TButton', 
                  foreground=letra_botao_menu, 
                  background=fundo_botao_menu,
                  font=('Helvetica', 14, 'bold'),
                  padding=10,
                  borderwidth=2,
                  relief="solid")
    
    # Estilo quando botão é pressionado
    style.map('Game.TButton',
             foreground=[('pressed', AZUL_SENAC), ('active', AZUL_SENAC)],
             background=[('pressed', LARANJA_CLARO), ('active', LARANJA_CLARO)])
    
    style.map('Action.TButton',
             foreground=[('pressed', AZUL_SENAC), ('active', AZUL_SENAC)],
             background=[('pressed', LARANJA_CLARO), ('active', LARANJA_CLARO)])
    
    app = MainApplication(root)
    root.mainloop()
