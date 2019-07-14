class Pessoa:
    def __init__(self, nome = 'Inimigo'):
        self.nome = nome
        self.vida = 100
        self.ataque = 1
        self.defesa = 0
        self.nivel = 0
        self.gloria = 0
        self.total = {'vida': self.vida, 'ataque': self.ataque, 'defesa': self.defesa}

    def __sub__(self, inimigo):
        if inimigo.ataque == self.defesa: print('Ataque defendido totalmente')
        elif inimigo.ataque < self.defesa:
            inimigo - self
            print('Contra-ataque!')
        else:
            self.vida -= inimigo.ataque - self.defesa
            print(self.nome, 'recebeu',inimigo.ataque-self.defesa, 'de dano!')
        if 0 < self.vida < 10:
            print(self.nome, 'está muito ferido!')
            self.ataque = 1
            self.defesa = 1
        elif self.vida < 0:
            print(self.nome, 'morreu.')
            del(self) # ????????????

    def __add__(self, pocao):
        self.vida += pocao.cont
        if self.vida > self.total['vida']: self.vida = self.total['vida']

    def __str__(self):
        for i,o in self.__dict__.items():
            print(i+':',o)
        return str(self.__dict__)

    def up(self):
        self.gloria -= 100
        if self.gloria > 99: self.descansa()
        self.total['vida'] += 10
        self.vida = self.total['vida']
        self.total['ataque'] += 1
        self.ataque = self.total['ataque']
        self.total['defesa'] += 1
        self.defesa = self.total['defesa']
        self.nivel += 1
    
    def heal(self, quant):
        self.vida += quant
        if self.vida > self.total['vida']: self.vida = self.total['vida']

    def descansa(self):
        if self.gloria > 99: self.up()
        else:
            self.heal()
