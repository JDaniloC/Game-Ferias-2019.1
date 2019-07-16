from tkinter import *
import random
import time
from Classes import Pessoa

class mob(Pessoa):
    def __init__(self, canvas, cor, nome = "inimigo"):
        self.canvas = canvas
        super().__init__(nome)
        self.id = canvas.create_oval(10,10,25,25, fill= cor)
        self.canvas.move(self.id, random.randrange(0,580,2), random.randrange(0,580,2))
        if cor == "green":
            self.canvas.bind_all("<Key-a>", self.esquerda)
            self.canvas.bind_all("<Key-d>", self.direita)
            self.canvas.bind_all("<Key-w>", self.cima)
            self.canvas.bind_all("<Key-s>", self.baixo)
        elif cor == "blue":
            self.canvas.bind_all("<KeyPress-Left>", self.esquerda)
            self.canvas.bind_all("<KeyPress-Right>", self.direita)
            self.canvas.bind_all("<KeyPress-Up>", self.cima)
            self.canvas.bind_all("<KeyPress-Down>", self.baixo)

    def __eq__(self, outro):
        if self.posicao() == outro.posicao(): return True
        return False

    def esquerda(self, evt):
        if self.posicao()[0] > 1:
            self.canvas.move(self.id, -2,0)
        self.posicao()
    def direita(self, evt):
        if self.posicao()[0] < 580:
            self.canvas.move(self.id, 2,0)
        self.posicao()
    def cima(self, evt):
        if self.posicao()[1] > 1:
            self.canvas.move(self.id, 0,-2)
        self.posicao()
    def baixo(self, evt):
        if self.posicao()[1] < 580:
            self.canvas.move(self.id, 0,2)
        self.posicao()
    def anda(self):
        lista = [-2,0,2]
        random.shuffle(lista)
        self.canvas.move(self.id, lista[0], lista[1])

    def posicao(self):
        return self.canvas.coords(self.id)

    def printa(self, evt):
        print(evt)

def dano(atk, dfs):
    atk - dfs
    dfs - atk
    print(atk.nome+":",atk.vida)
    print(dfs.nome+":",dfs.vida)

def igual(locais):
    if locais == []: return
    for i in locais[1:]:
        if locais[0].posicao() == i.posicao():
            dano(locais[0], i)
    return igual(locais[1:])

janela = Tk()
janela.title("A abolição do homem.")

janela.resizable(0,0)
janela.wm_attributes("-topmost", 1)

tela = Canvas(janela, width=600, height=600, bd=0, highlightthickness=0)
botao = Button(janela, text="Pausa!", command=lambda: time.sleep(2))
tela.pack()
botao.pack()

jogador = mob(tela, "blue", "Azul")
outro = mob(tela, "green", "Verde")
inimigo = mob(tela, "red")
locais = [jogador, outro, inimigo]

while True:
    janela.update_idletasks()
    janela.update()
    igual(locais)
    for i in range(len(locais)-1, 0, -1):
        if locais[i].vida == 0:
            del locais[i]
            locais.pop(i)
    inimigo.anda()
    time.sleep(0.05)