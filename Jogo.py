from tkinter import *
import random
import time
from Classes import Pessoa, Supply, Xp
from math import sqrt
from functools import partial
from tkinter import messagebox
from Multilistbox import Multilist

class Mob(Pessoa):
    listaNegra = []
    def __init__(self, canvas, cor, nome = "inimigo"):
        self.cor = cor
        self.canvas = canvas
        super().__init__(nome)
        self.id = canvas.create_oval(10,10,26,26, fill= cor)
        if nome == "inimigo": nome = cor
        self.info = canvas.create_text(30,5, text=nome)
        self.canvas.move(self.id, random.randrange(0,1240,2), random.randrange(0,680,2))
        self.canvas.move(self.info, self.posicao()[0]-20, self.posicao()[1]-12)
        if self.cor == "green":
            self.canvas.bind_all("<Key-a>", self.esquerda)
            self.canvas.bind_all("<Key-d>", self.direita)
            self.canvas.bind_all("<Key-w>", self.cima)
            self.canvas.bind_all("<Key-s>", self.baixo)
        elif self.cor == "blue":
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
            self.canvas.move(self.info, -2,0)
        self.posicao()
    def direita(self, evt = None):
        if self.posicao()[0] < 1240:
            self.canvas.move(self.id, 2,0)
            self.canvas.move(self.info, 2,0)
        self.posicao()
    def cima(self, evt = None):
        if self.posicao()[1] > 1:
            self.canvas.move(self.id, 0,-2)
            self.canvas.move(self.info, 0, -2)
        self.posicao()
    def baixo(self, evt = None):
        if self.posicao()[1] < 680:
            self.canvas.move(self.id, 0,2)
            self.canvas.move(self.info, 0, 2)
        self.posicao()
    def aleatorio(self):
        lista = [self.esquerda, self.direita, self.cima, self.baixo]
        random.shuffle(lista)
        lista[0]()
    def npc(self, mobs):
        if self.cor != 'blue' and self.cor != 'green':
            pos = self.posicao()
            if self.vida > 10:
                if self.nivel > 1: objetivo = self.calcula(mobs['pl']+mobs['pw'])
                elif len(mobs['pw']) > 0: objetivo = self.calcula(mobs['pw'])
                else: objetivo = self.calcula(mobs['pl'])
                self.persegue(pos, objetivo)
            else:
                if len(mobs['pw']) > 0:
                    objetivo = self.calcula(mobs['pw'])
                    self.persegue(pos, objetivo)
                else:
                    objetivo = self.calcula(mobs['pl'])
                    self.foge(pos, objetivo)
    
    def persegue(self, pos, objetivo):
        if random.randint(1,2) == 1:
            if objetivo[1] < pos[1]: self.cima()
            elif objetivo[3] > pos[3]: self.baixo()
        else:
            if objetivo[0] < pos[0]: self.esquerda()
            elif objetivo[2] > pos[2]: self.direita()
    def foge(self, pos, objetivo):
        if random.randint(1,2) == 1:
            if objetivo[1] <= pos[1]: self.baixo()
            elif objetivo[3] > pos[3]: self.cima()
        else:
            if objetivo[0] <= pos[0]: self.direita()
            elif objetivo[2] > pos[2]: self.esquerda()

    def calcula(self, mobs):
        coords = self.posicao()[:2]
        dist = []
        for i in mobs:
            if i.id != self.id and i.id not in self.listaNegra:
                cords = i.posicao()[:2]
                dist.append(sqrt((abs(coords[0]-cords[0]))**2+(abs(coords[1]-cords[1]))**2))
            elif i.id in self.listaNegra:
                dist.append(9998)
            else: dist.append(9999)
        return mobs[dist.index(min(dist))].posicao()

    def posicao(self):
        return self.canvas.coords(self.id)

    def deleta(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.info)

    def eventos(self, evt):
        print(evt)

class Ob(Xp):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="yellow")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,670,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)

class Ob2(Supply):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="brown")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,670,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)

class NaoJogo:
    def __init__(self, janela, jogadores, mobs, opcao, frequencia):
        self.verificador = True
        janela.destroy()
        self.janela = Tk()
        self.janela.title("A abolição do homem")

        self.janela.resizable(0,0)
        self.janela.wm_attributes("-topmost", 1)

        fram = Frame(self.janela)
        tela = Canvas(fram, width=1280, height=700, bd=0, highlightthickness=0)
        pontos = Frame(fram, height=700)
        lb = Label(pontos, text="Pontuação", font="Georgia 20 bold")
        frame = Frame(self.janela)
        botao = Button(frame, text="Pausa!", command=lambda: time.sleep(30))
        vaza = Button(frame, text="Sair!", command=self.sair)
        fram.pack()
        tela.pack(side=LEFT)
        pontos.pack(side=RIGHT)
        lb.pack()
        frame.pack()
        botao.pack(side="left")
        vaza.pack(side='left')

        cores = ['navy', 'cornflower blue', 'dark slate blue', 'light sea green', 'lawn green', 'lime green', 'dark khaki', 'goldenrod',  'rosy brown','indian red', 'saddle brown', 'dark orange', 'red', 'hot pink', 'pale violet red', 'maroon', 'snow4', 'SlateBlue1', 'DeepSkyBlue2', 'turquoise1', 'SeaGreen1', 'OliveDrab1']

        self.players = []
        powerups = []

        for i in range(jogadores):
            self.players.append(Mob(tela, cores[i], cores[i]))
        for i in range(mobs):
            powerups.append(Ob(tela))
            powerups.append(Ob2(tela))

        if opcao  == 1:
            self.players.append(Mob(tela, 'blue', "Jogador"))
        elif opcao == 2:
            self.players.append(Mob(tela, 'blue', "Jogador 01"))
            self.players.append(Mob(tela, 'green', 'Jogador 02'))

        objetos = {'pl':self.players, 'pw':powerups}
        cont = 0
        self.pn = Multilist(pontos, 9, (("Nome", 15), ("Nível", 1)))
        self.pp = Multilist(pontos, 9, (("Nome", 15), ("Pontos", 1)))
        self.pa = Multilist(pontos, 9, (("Nome", 15), ("Ataque", 1)))
        self.pd = Multilist(pontos, 9, (("Nome", 15), ("Defesa", 1)))
        self.atualiza()
        self.pp.pack(expand=YES, fill=BOTH)
        self.pn.pack(expand=YES, fill=BOTH)
        self.pa.pack(expand=YES, fill=BOTH)
        self.pd.pack(expand=YES, fill=BOTH)
        while self.verificador:
            cont += 1
            if cont % (100*frequencia) == 0:
                powerups.append(Ob(tela))
                powerups.append(Ob2(tela))
            if cont % 300 == 0:
                self.atualiza()
                for i in self.players:
                    i.listaNegra = []
            if cont == 600: cont = 0
            self.janela.update_idletasks()
            self.janela.update()
            for i in self.players:
                i.npc(objetos)
            random.shuffle(self.players)
            self.igual(self.players)
            self.igual2(self.players, powerups)
            time.sleep(0.01)
            if len(self.players) < 2:
                break
        messagebox.showinfo("Fim de Jogo", self.players[0].nome+' venceu o jogo!' )
        ganhador = self.players[0].__dict__
        lista = ["vida", "ataque", "defesa", "nivel", "gloria", "total"]
        print("Informações de", ganhador["nome"])
        for i in lista:
            print(i,":",ganhador[i])
        self.sair()
    
    def sair(self):
        self.verificador = False
        self.janela.destroy()
    
    def atualiza(self):
        self.pn.delete(0, END)
        self.pp.delete(0, END)
        self.pa.delete(0, END)
        self.pd.delete(0, END)
        self.players.sort(reverse=True)
        for i in self.players:
            self.pn.insert(END, (i.nome, i.nivel))
            self.pp.insert(END, (i.nome, i.pontos))
            self.pa.insert(END, (i.nome, i.ataque))
            self.pd.insert(END, (i.nome, i.defesa))

    def compara(self, l1, l2):
        if l1[0] <= l2[0]:
            if l1[1] <= l2[1]:
                if l1[2] >= l2[2]:
                    if l1[3] >= l2[3]:
                        return True
        return False
    
    def dano(self, atk, dfs):
        if dfs - atk != 1:
            atk.listaNegra.append(dfs.id)
        atk - dfs
        print(atk.nome+":",atk.vida)
        print(dfs.nome+":",dfs.vida)
        try:
            if atk.vida < 1:
                dfs + Xp()
                dfs + Supply()
                atk.deleta()
                self.players.remove(atk)
                del atk
            if dfs.vida < 1:
                atk + Xp()
                atk + Supply()
                dfs.deleta()
                self.players.remove(dfs)
                del dfs
        except:
            print("Deu erro!")

    def igual(self, locais): # Antes era recursivo e chegava ao máximo
        for a in range(len(locais)):
            for i in range(a+1,len(locais)):
                if i < len(locais) and a < len(locais):
                    if locais[a].posicao() == locais[i].posicao():
                        self.dano(locais[a], locais[i])
    
    def igual2(self, jogadores, objetos):
        for a in range(len(jogadores)):
            for i in objetos:
                if self.compara(jogadores[a].posicao(), i.posicao()):
                    jogadores[a] + i
                    i.deleta()
                    objetos.remove(i)
                    del i
    

class config:
    def __init__(self):
        janela = Tk()
        escolha = IntVar()
        self.frequencia = IntVar()
        janela.title("Configurações")
        label = Label(janela, text='Quantos Jogadores?')
        entry = Entry(janela)
        label2 = Label(janela, text='Quantos recursos?')
        entry2 = Entry(janela)
        label3 = Label(janela, text='Haverão jogadores?')
        check = Radiobutton(janela, text= "Apenas NPC\'s", variable=escolha, value=0)
        check2 = Radiobutton(janela, text= "Um jogador nas setas", variable=escolha, value=1)
        check3 = Radiobutton(janela, text= "Dois jogadores (WASD)", variable=escolha, value=2)
        label4 = Label(janela, text='Frequência de respawn')
        frame = Frame(janela)
        chequi =  Radiobutton(frame, text="0", variable= self.frequencia, value=10)
        chequi1 = Radiobutton(frame, text="1", variable= self.frequencia, value=5)
        chequi2 = Radiobutton(frame, text="2", variable= self.frequencia, value=3)
        chequi3 = Radiobutton(frame, text="3", variable= self.frequencia, value=1)
        comecar = Button(janela, text="Iniciar", command=partial(self.inicia, janela, entry, entry2, escolha))
        label.pack()
        entry.pack()
        label2.pack()
        entry2.pack()
        label3.pack()
        check.pack()
        check2.pack()
        check3.pack()
        label4.pack()
        frame.pack()
        chequi.pack(side=LEFT)
        chequi1.pack(side=LEFT)
        chequi2.pack(side=LEFT)
        chequi3.pack(side=LEFT)
        comecar.pack()
        chequi.select()
        janela.mainloop()

    def inicia(self, janela, entry, entry2, escolha):
        entry, entry2, escolha, frequencia = entry.get(), entry2.get(), escolha.get(), self.frequencia.get()
        verificator = True
        if entry == '' or entry2 == '':
            verificator = False
            messagebox.showinfo("Alerta", "Preencha os campos!")
        elif not entry.isnumeric() or not entry2.isnumeric():
            verificator = False
            messagebox.showinfo("Alerta", "Precisa ser um número!")
        elif 9 < int(entry) < 23:
            messagebox.showinfo("Alerta", "Você colocou mais de 9 jogadores! Pode dar uma excessão!") 
        elif int(entry) > 22:
            verificator = False
            messagebox.showinfo("Alerta", "Você ultrapassou o máximo de jogadores (22)!")
        elif int(entry2) > 100:
            messagebox.showinfo("Alerta", "Haverá mais de 200 objetos na tela! Pode ficar lento!")
        if verificator:
            NaoJogo(janela, int(entry), int(entry2), escolha, frequencia)
config()