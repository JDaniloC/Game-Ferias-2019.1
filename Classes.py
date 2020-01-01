from tkinter import *
from math import sqrt
import random

class Pessoa:
    def __init__(self, nome = 'Inimigo'):
        self.nome = nome
        self.vida = 100
        self.ataque = 1
        self.defesa = 0
        self.nivel = 0
        self.gloria = 0
        self.pontos = self.ataque*5+self.defesa*4+self.nivel*self.vida/100+self.gloria
        self.total = {'vida': self.vida, 'ataque': self.ataque, 'defesa': self.defesa}

    def __sub__(self, inimigo):
        if inimigo.ataque == self.defesa: 
            #print('Ataque defendido totalmente')
            return 0
        elif inimigo.ataque < self.defesa:
            return 2
        else:
            self.vida -= inimigo.ataque - self.defesa
            #print(self.nome, 'recebeu',inimigo.ataque-self.defesa, 'de dano!')
        if 0 < self.vida < 10:
            #print(self.nome, 'está muito ferido!')
            self.ataque = self.total['ataque']
            self.defesa = self.total['defesa']
        elif self.vida < 1:
            #print(self.nome, 'morreu.')
            self.__del__()
        return 1

    def __add__(self, pocao):
        try:
            pocao = pocao.eat()
            if pocao > 5: self.vida += pocao
            elif pocao == 5: self.ataque += pocao
            else: self.defesa += pocao
            if self.vida > self.total['vida']: self.vida = self.total['vida']
        except:
            self.gloria += pocao.tipo
            if self.gloria > 99: self.up()
        #finally:
        #    print(self)

    def __str__(self):
        for i,o in self.__dict__.items():
            print(i+':',o)
        print()
        return str(self.__dict__)
    
    def __del__(self):
        print(self.nome,"morreu ao nível:",self.nivel)

    def __gt__(self, outro): # a grande sacada pra fazer sort()
        if self.pontos > outro.pontos: return True
        return False
    
    def up(self):
        self.gloria -= 100
        self.total['vida'] += 10
        self.vida = self.total['vida']
        self.total['ataque'] += 1
        self.ataque = self.total['ataque']
        self.total['defesa'] += 1
        self.defesa = self.total['defesa']
        self.nivel += 1
        self.pontos = self.ataque*5+self.defesa*4+self.nivel*self.vida/100+self.gloria
        if self.gloria > 99: self.up()

class Supply:
    def __init__(self):
        self.tipo = random.randint(1,5)
    def eat(self):
        if self.tipo == 1:
            print("Poção Simples!")
            return 10
        elif self.tipo == 2:
            print("Poção Normal!")
            return 50
        elif self.tipo == 3:
            print("Poção Grande!")
            return 100
        elif self.tipo == 4:
            print("Mais força!")
            return 5
        else:
            print("Mais defesa!")
            return 3

class Xp:
    def __init__(self): 
        self.lista = [10, 50, 100]
        random.shuffle(self.lista)
        self.tipo = self.lista[0]

class Mob(Pessoa):
    '''
    A uniao da classe Pessoa com as peculiaridades de funcoes atraves do Tkinter como:
     - Se movimentar (teleportar 2 pixels):
        . Movimento lento e rapido para players
        . Movimento aleatorio para Bots
        . Movimento inteligente para Bots
     - Reconhecer e retornar localizacao
     - Se auto deletar

Funções:
    1 - __init__(canvas, cor, nome = "inimigo", mov = "n")
        Quando instanciar o objeto Mob, ele recebe pelo menos a cor do objeto, para ser exibido no Tkinter
            - canvas = O objeto Canvas (tkinter) onde o objeto Mob sera instanciado
            - nome   = Caso quiser colocar um nome na hora da vitoria
            - mov    = Se ele deve andar automaticamente (na direcao dada) ou nao

    2 - __eq__(outro)
        Para comparar objetos, através da localização deles, e saber se eles se encontraram.
            - outro = O outro objeto que ira ser comparado
    
    3 - para(evt = None)
        Para a movimentacao do jogador se o mesmo estiver em movimento automatico
            - evt = O evento que faz com que ele pare (Shift ou Ctrl)

    4 - acima(evt = None), abaixo(evt = None), aesquerda(evt = None), adireita(evt = None)
        Para a movimentacao automatica do jogador apenas mudando uma expressao booleana
            - evt = O evento que faz com que ele mude (setas ou WASD)
    
    5 - cima(evt = None), baixo(evt = None), esquerda(evt = None), direita(evt = None)
        Para a movimentacao por passos para qualquer Mob
            - evt = O evento que faz com que ele mude (setas ou WASD)
    
    6 - aleatorio()
        Faz o Mob andar aleatoriamente
    
    7 - npc(mobs)
        Faz o Mob pensar qual lista de objetos tentar seguir/fugir (outros Mobs ou outro objeto)
        Ele considera o proprio life e se as listas dadas tem itens
            - mobs = Lista de objetos (Mobs e outros objetos)
    
    8 - persegue(pos, objetivo), foge(pos, objetivo)
        Analisa a posicao atual e qual o objetivo dado e vai em direcao ou em direcao contraria
            - pos      = Posicao atual
            - objetivo = Posicao do alvo

    10 - calcula(mobs)
        Analisa qual o objeto mais proximo para seguir
            - mobs = Lista de objetos

    11 - posicao()
        Devolve a posicao do objeto Mob

    12 - deleta()
        Deleta o canvas que eh o proprio objeto Mob
    '''
    def __init__(self, canvas, cor, nome = "inimigo", mov = 'n'):
        self.listaNegra = []
        self.mov = mov
        self.movimentos = [False, False, False, False] # 0 = Cima, 1 = Baixo, 2 = Esquerda, 3 = Direita
        self.cor = cor
        self.canvas = canvas
        super().__init__(nome)
        self.id = canvas.create_oval(10,10,26,26, fill= cor)
        if nome == "inimigo": nome = cor
        self.info = canvas.create_text(30,5, text=nome)
        self.life = canvas.create_text(30,5, text=str(self.vida))
        self.canvas.move(self.id, random.randrange(0,1240,2), random.randrange(0,680,2))
        self.canvas.move(self.info, self.posicao()[0] - 20, self.posicao()[1] - 12)
        self.canvas.move(self.life, self.posicao()[0] - 22, self.posicao()[1] + 18)
        if self.cor == "green":
            self.canvas.bind_all("<Shift_L>", self.para)
            if self.mov == 'n':
                self.canvas.bind_all("<Key-a>", self.esquerda)
                self.canvas.bind_all("<Key-d>", self.direita)
                self.canvas.bind_all("<Key-w>", self.cima)
                self.canvas.bind_all("<Key-s>", self.baixo)
            else:
                self.canvas.bind_all("<Key-a>", self.aesquerda)
                self.canvas.bind_all("<Key-d>", self.adireita)
                self.canvas.bind_all("<Key-w>", self.acima)
                self.canvas.bind_all("<Key-s>", self.abaixo)
        elif self.cor == "blue":
            self.canvas.bind_all("<Control_R>", self.para)
            if self.mov == 'n':
                self.canvas.bind_all("<KeyPress-Left>", self.esquerda)
                self.canvas.bind_all("<KeyPress-Right>", self.direita)
                self.canvas.bind_all("<KeyPress-Up>", self.cima)
                self.canvas.bind_all("<KeyPress-Down>", self.baixo)
            else:
                self.canvas.bind_all("<KeyPress-Left>", self.aesquerda)
                self.canvas.bind_all("<KeyPress-Right>", self.adireita)
                self.canvas.bind_all("<KeyPress-Up>", self.acima)
                self.canvas.bind_all("<KeyPress-Down>", self.abaixo)

    def __eq__(self, outro):
        if self.posicao() == outro.posicao(): return True
        return False
    
    def para(self, evt=None):
        for i in range(len(self.movimentos)):
            self.movimentos[i] = False

    def acima(self, evt=None): 
        for i in range(len(self.movimentos)):
            self.movimentos[i] = False
        self.movimentos[0] = True
    def abaixo(self, evt=None): 
        for i in range(len(self.movimentos)):
            self.movimentos[i] = False
        self.movimentos[1] = True
    def aesquerda(self, evt=None): 
        for i in range(len(self.movimentos)):
            self.movimentos[i] = False
        self.movimentos[2] = True
    def adireita(self, evt=None): 
        for i in range(len(self.movimentos)):
            self.movimentos[i] = False
        self.movimentos[3] = True

    def esquerda(self, evt = None):
        if self.posicao()[0] > 1:
            self.canvas.move(self.id, -2,0)
            self.canvas.move(self.info, -2,0)
            self.canvas.move(self.life, -2,0)
        self.posicao()
    def direita(self, evt = None):
        if self.posicao()[0] < 1240:
            self.canvas.move(self.id, 2,0)
            self.canvas.move(self.info, 2,0)
            self.canvas.move(self.life, 2,0)
        self.posicao()
    def cima(self, evt = None):
        if self.posicao()[1] > 1:
            self.canvas.move(self.id, 0,-2)
            self.canvas.move(self.info, 0, -2)
            self.canvas.move(self.life, 0, -2)
        self.posicao()
    def baixo(self, evt = None):
        if self.posicao()[1] < 680:
            self.canvas.move(self.id, 0,2)
            self.canvas.move(self.info, 0, 2)
            self.canvas.move(self.life, 0, 2)
        self.posicao()

    def aleatorio(self):
        lista = [self.esquerda, self.direita, self.cima, self.baixo]
        random.shuffle(lista)
        lista[0]()
    def npc(self, mobs):
        if self.cor not in ['blue', 'green', 'coral1', 'bisque2', 'aquamarine', 'OliveDrab1']:
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
            else: dist.append(9999) # Eu podia colocar float('inf') mas não importa muito.
        return mobs[dist.index(min(dist))].posicao()

    def posicao(self):
        return self.canvas.coords(self.id)

    def deleta(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.info)
        self.canvas.delete(self.life)

    def json(self):
        # nome, nível, pontos, ataque, defesa, local
        return {"nome": self.nome, "cor": self.cor, "vida":self.vida, "nivel": self.nivel, "pontos": self.pontos, "ataque": self.ataque, "defesa": self.defesa, "posicao": self.posicao()}

class Ob(Xp):
    '''
    Objeto de tradução da classe Xp para tkinter
    '''
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="yellow")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,670,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)
    def json(self):
        return {"cor":'yellow', "id": self.id, "posicao": self.posicao()}

class Ob2(Supply):
    '''
    Objeto de tradução da classe Supply para tkinter
    '''
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.id = canvas.create_oval(10,10,20,20,fill="brown")
        self.canvas.move(self.id, random.randrange(0,1200,2), random.randrange(0,670,2))
    def posicao(self):
        return self.canvas.coords(self.id)
    def deleta(self):
        self.canvas.delete(self.id)
    def json(self):
        return {"cor":'brown', "posicao": self.posicao()}
