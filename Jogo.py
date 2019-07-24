from tkinter import *
import random
import time
from Classes import Pessoa, Supply, Xp
from math import sqrt

class Mob(Pessoa):
    def __init__(self, canvas, cor, nome = "inimigo"):
        self.canvas = canvas
        super().__init__(nome)
        self.id = canvas.create_oval(10,10,26,26, fill= cor)
        self.canvas.move(self.id, random.randrange(0,1240,2), random.randrange(0,730,2))
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

    def esquerda(self, evt = None):
        if self.posicao()[0] > 1:
            self.canvas.move(self.id, -2,0)
        self.posicao()
    def direita(self, evt = None):
        if self.posicao()[0] < 1240:
            self.canvas.move(self.id, 2,0)
        self.posicao()
    def cima(self, evt = None):
        if self.posicao()[1] > 1:
            self.canvas.move(self.id, 0,-2)
        self.posicao()
    def baixo(self, evt = None):
        if self.posicao()[1] < 730:
            self.canvas.move(self.id, 0,2)
        self.posicao()
    def aleatorio(self):
        lista = [self.esquerda, self.direita, self.cima, self.baixo]
        random.shuffle(lista)
        lista[0]()
    def anda(self, objetivo):
        pos = self.posicao()
        if random.randint(1,2) == 1:
            if objetivo[1] < pos[1]: self.cima()
            elif objetivo[3] > pos[3]: self.baixo()
        else:
            if objetivo[0] < pos[0]: self.esquerda()
            elif objetivo[2] > pos[2]: self.direita()

    def calcula(self, mobs):
        coords = self.posicao()[:2]
        dist = []
        for i in mobs:
            if i.id != self.id:
                cords = i.posicao()[:2]
                dist.append(sqrt((abs(coords[0]-cords[0]))**2+(abs(coords[1]-cords[1]))**2))
            else: dist.append(9999)
        self.anda(mobs[dist.index(min(dist))].posicao())

    def posicao(self):
        return self.canvas.coords(self.id)

    def deleta(self):
        self.canvas.delete(self.id)

    def eventos(self, evt):
        print(evt)

class Ob(Xp):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="yellow")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,700,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)

class Ob2(Supply):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="brown")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,700,2))
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

def sair():
    global verificador
    verificador = False

janela = Tk()
janela.title("A abolição do homem.")

janela.resizable(0,0)
janela.wm_attributes("-topmost", 1)

tela = Canvas(janela, width=1280, height=750, bd=0, highlightthickness=0)
frame = Frame(janela)
botao = Button(frame, text="Pausa!", command=lambda: time.sleep(2))
vaza = Button(frame, text="Sair!", command=sair)
tela.pack()
frame.pack()
botao.pack(side="left")
vaza.pack(side='left')

cores = ['dark slate gray', 'dim gray', 'slate gray', 'navy', 'cornflower blue', 'dark slate blue', 'deep sky blue', 'medium aquamarine', 'dark green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green','lawn green', 'green yellow', 'lime green', 'olive drab', 'dark khaki', 'gold', 'goldenrod',  'rosy brown','indian red', 'saddle brown', 'dark orange', 'red', 'hot pink', 'pale violet red', 'maroon', 'medium orchid', 'medium purple', 'snow4', 'SlateBlue1', 'DeepSkyBlue2', 'turquoise1', 'SeaGreen1', 'SpringGreen2', 'OliveDrab1']

locais = []
for i in cores:
    locais.append(Mob(tela, i, i))
locais2 = []
for i in range(50):
    locais2.append(Ob(tela))
    locais2.append(Ob2(tela))

verificador = True
while verificador:
    janela.update_idletasks()
    janela.update()
    igual(locais)
    igual2(locais, locais2)
    for i in locais:
        i.calcula(locais+locais2)
    time.sleep(0.05)
