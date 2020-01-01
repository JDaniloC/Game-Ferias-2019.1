from tkinter import *
from tkinter import messagebox
from functools import partial
from BackEnd import Game, Client
from Udp import Internet

'''
Criando um "Jogo" simples em Tkinter!
'''

class config:
    '''
    A classe de configuração, logo, início do game.

Funções:
    1 - __init__()
        Onde será escolhido todas as configurações para entrar no game.
    
    2 - inicia(janela)
        Onde irá verificar se todas as informações batem corretamente, e começa o game.
    '''
    def __init__(self): # Colocar a opção de online e criar uma nova classe client.
        janela = Tk()
        self.servidor = None
        self.escolha = IntVar()
        self.vlc = DoubleVar()
        self.frequencia = IntVar()
        self.choice = IntVar()
        janela.title("Configurações")
        Label(janela, text='Quantos Jogadores?').pack()
        self.entrada = Scale(janela, to = 22, orient = HORIZONTAL, length = 200) # No máximo 22 pra ter cores únicas!
        self.entrada.pack()
        Label(janela, text='Quantos recursos?').pack()
        self.entrada2 = Scale(janela, to = 200, orient = HORIZONTAL, length = 200)
        self.entrada2.pack()
        Label(janela, text='Haverão jogadores?').pack()
        Radiobutton(janela, text = "Apenas NPC\'s", variable = self.escolha, value = 0).pack(anchor = 'w')
        Radiobutton(janela, text = "Um jogador nas setas", variable = self.escolha, value = 1).pack(anchor = 'w')
        Radiobutton(janela, text = "Dois jogadores (WASD)", variable = self.escolha, value = 2).pack(anchor = 'w')
        Radiobutton(janela, text = "Online - single - servidor", variable = self.escolha, value = 3, command = self.server).pack(anchor = 'w')
        Radiobutton(janela, text = "Online - coop - servidor", variable = self.escolha, value = 4, command = self.server).pack(anchor = 'w')
        Radiobutton(janela, text = "Online - cliente", variable = self.escolha, value = 5, command = self.client).pack(anchor = 'w')
        Label(janela, text='Frequência de respawn').pack()
        frame = Frame(janela)
        frame.pack()
        chequi =  Radiobutton(frame, text="0", variable= self.frequencia, value=10)
        chequi.pack(side=LEFT)
        Radiobutton(frame, text="1", variable= self.frequencia, value=5).pack(side=LEFT)
        Radiobutton(frame, text="2", variable= self.frequencia, value=3).pack(side=LEFT)
        Radiobutton(frame, text="3", variable= self.frequencia, value=1).pack(side=LEFT)
        Label(janela, text="Nível de velocidade").pack()
        frame2 = Frame(janela)
        frame2.pack()
        Radiobutton(frame2, text="1", variable= self.vlc, value=0.5).pack(side=LEFT)
        Radiobutton(frame2, text="2", variable= self.vlc, value=0.1).pack(side=LEFT)
        Radiobutton(frame2, text="3", variable= self.vlc, value=0.05).pack(side=LEFT)
        Radiobutton(frame2, text="4", variable= self.vlc, value=0.035).pack(side=LEFT)
        xeq5 = Radiobutton(frame2, text="5", variable= self.vlc, value=0.01)
        xeq5.pack(side=LEFT)
        Radiobutton(frame2, text="6", variable= self.vlc, value=0.001).pack(side=LEFT)
        Radiobutton(frame2, text="7", variable= self.vlc, value=0).pack(side=LEFT)
        auto = Checkbutton(janela, text="Movimento Automático?", variable=self.choice)
        auto.pack()
        Button(janela, text="Iniciar", command=partial(self.inicia, janela)).pack()
        chequi.select()
        xeq5.select()
        auto.select()
        janela.mainloop()

    def server(self):
        if self.servidor == None:
            self.servidor = Internet(1777)
            self.status = Label(text = 'Clients no momento: 0')
            self.status.pack()
        pop = Tk()
        Label(pop, text = "Clique em procurar para adicionar novos clientes.").pack()
        Button(pop, text = "Procurar", command = self.search).pack()

    def search(self):
        resultado = self.servidor.conectarServidor()
        self.status['text'] = "Clients no momento: "+ str(len(self.servidor))

    def client(self):
        if self.servidor == None:
            self.servidor = Internet()
        self.pop = Tk()
        Label(self.pop, text = "Ponha o IP e clique em tentar para conectar com o servidor.").grid(row = 0, columnspan = 2)
        self.ip = Entry(self.pop)
        self.ip.insert(END, '127.0.0.1')
        self.ip.grid(row = 1, columnspan = 2)
        Button(self.pop, text = "Tentar", command = self.connect).grid(row = 2, columnspan = 2)
    
    def connect(self):
        ip = self.ip.get()
        if self.servidor.conectarClient(ip, 1777) == "OK":
            self.pop.destroy()
            self.status = Label(text = f"Você é o cliente {str(self.servidor.id)}")
            self.status.pack()
        else:
            self.status['text'] = "Tente de novo... "

    def inicia(self, janela):
        entrada, entrada2, escolha, frequencia, velocidade = self.entrada.get(), self.entrada2.get(), self.escolha.get(), self.frequencia.get(), self.vlc.get()
        verificator = True
        if velocidade == 0:
            messagebox.showwarning("Alerta", "Velocidade nível computador, apenas para testes!")
        if verificator:
            janela.destroy()
            if escolha != 5:
                if self.choice.get() == 1: Game(entrada, entrada2, escolha, frequencia, velocidade, 's', self.servidor)
                else: Game(entrada, entrada2, escolha, frequencia, velocidade, 'n', self.servidor)
            else:
                Client(self.servidor.id, self.servidor)

if __name__ == "__main__":
    config()
