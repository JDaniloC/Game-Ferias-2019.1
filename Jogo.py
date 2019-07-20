from tkinter import *
import random
import time
from Classes import Pessoa, Supply, Xp

class mob(Pessoa):
    def __init__(self, canvas, cor, nome = "inimigo"):
        self.canvas = canvas
        super().__init__(nome)
        self.id = canvas.create_oval(10,10,26,26, fill= cor)
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

    def deleta(self):
        self.canvas.delete(self.id)

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

class Ob(Xp):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="yellow")
        self.canvas.move(self.id, random.randrange(0,580,2), random.randrange(0,580,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)

class Ob2(Supply):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="brown")
        self.canvas.move(self.id, random.randrange(0,580,2), random.randrange(0,580,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)

def compara(l1, l2):
    if l1[0] <= l2[0]:
        if l1[1] <= l2[1]:
            if l1[2] >= l2[2]:
                if l1[3] >= l2[3]:
                    return True
    return False

def dano(atk, dfs):
    global locais
    atk - dfs
    dfs - atk
    print(atk.nome+":",atk.vida)
    print(dfs.nome+":",dfs.vida)
    if atk.vida < 1:
        atk.deleta()
        locais.remove(atk)
        del atk
    if dfs.vida < 1:
        dfs.deleta()
        locais.remove(dfs)
        del dfs

def igual(locais):
    if locais == []: return
    for i in locais[1:]:
        if locais[0].posicao() == i.posicao():
            dano(locais[0], i)
    return igual(locais[1:])

def igual2(jogadores, objetos):
    if jogadores == []: return
    for i in objetos:
        if compara(jogadores[0].posicao(), i.posicao()):
            jogadores[0] + i
            i.deleta()
            objetos.remove(i)
            del i
    return igual2(jogadores[1:], objetos)

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
locais2 = []
for i in range(10):
    locais2.append(Ob(tela))
    locais2.append(Ob2(tela))

while True:
    print(jogador.posicao())
    print(locais2[0].posicao())
    janela.update_idletasks()
    janela.update()
    if len(locais) > 1: 
        igual(locais)
        igual2(locais, locais2)
    inimigo.anda()
    time.sleep(0.05)