from tkinter import *
from tkinter import messagebox
from backend.Classes import Supply, Xp, Mob, Ob, Ob2
from backend.Udp import Internet
from backend.Multilistbox import Multilist
import random, time, json

class Game:
    def __init__(self, jogadores = 3, mobs = 10, opcao = 0, frequencia = 5, velocidade = 0.01, auto = 's', internet = None):
        self.verificador = True
        self.janela = Tk()
        self.janela.title("A abolição do homem")

        self.janela.resizable(0,0)
        self.janela.wm_attributes("-topmost", 1)

        fram = Frame(self.janela)
        self.tela = Canvas(fram, width=1280, height=700, bd=0, highlightthickness=0)
        pontos = Frame(fram, height=700)
        lb = Label(pontos, text="Pontuação", font="Georgia 20 bold")
        frame = Frame(self.janela)
        botao = Button(frame, text="Pausa!", command=lambda: time.sleep(30))
        vaza = Button(frame, text="Sair!", command=self.sair)
        fram.pack()
        self.tela.pack(side=LEFT)
        pontos.pack(side=RIGHT)
        lb.pack()
        frame.pack()
        botao.pack(side="left")
        vaza.pack(side='left')

        cores = ['navy', 'cornflower blue', 'dark slate blue', 'light sea green', 'lawn green', 'lime green', 'dark khaki', 'goldenrod',  'rosy brown','indian red', 'saddle brown', 'dark orange', 'red', 'hot pink', 'pale violet red', 'maroon', 'snow4', 'SlateBlue1', 'DeepSkyBlue2', 'turquoise1', 'SeaGreen1', 'OliveDrab1']

        online = ['coral1', 'bisque2', 'aquamarine', 'OliveDrab1']
        self.players = []
        powerups = []

        # Adicionando jogadores
        if opcao > 0:
            if auto == 's':
                jogador = Mob(self.tela, 'blue', "Jogador 01", 's')
                self.players.append(jogador)
            else:
                self.players.append(Mob(self.tela, 'blue', "Jogador 01"))
        if opcao in [2, 4]:
            if auto == 's':
                jogador2 = Mob(self.tela, 'green', "Jogador 02", 's')
                self.players.append(jogador2)
            else:
                self.players.append(Mob(self.tela, 'green', "Jogador 02"))
        if opcao >= 3:
            for i in range(len(internet)):
                self.players.append(Mob(self.tela, random.choice(online), f"Jogador 0{i+3}"))
        for i in range(jogadores): # LIMITE DE JOGADORES!!
            self.players.append(Mob(self.tela, cores[i], cores[i])) # Se colocar um random aqui, não terá cores únicas :D
        for i in range(mobs):
            powerups.append(Ob(self.tela))
            powerups.append(Ob2(self.tela))

        self.objetos = {'pl':self.players, 'pw':powerups}
        cont = 0 # De frames

        # Os scores.
        self.pn = Multilist(pontos, 9, (("Nome", 15), ("Nível", 1)))
        self.pp = Multilist(pontos, 9, (("Nome", 15), ("Pontos", 1)))
        self.pa = Multilist(pontos, 9, (("Nome", 15), ("Ataque", 1)))
        self.pd = Multilist(pontos, 9, (("Nome", 15), ("Defesa", 1)))
        self.atualiza()
        self.pp.pack(expand=YES, fill=BOTH)
        self.pn.pack(expand=YES, fill=BOTH)
        self.pa.pack(expand=YES, fill=BOTH)
        self.pd.pack(expand=YES, fill=BOTH)
        while self.verificador: # Modificar para enviar certas informações!!
            cont += 1
            if cont % (100*frequencia) == 0: # Frequencia de aparecimento de PowerUps
                powerups.append(Ob(self.tela))
                powerups.append(Ob2(self.tela))
            if cont % 300 == 0: # Atualiza o placar
                self.atualiza()
                for i in self.players:
                    i.listaNegra = []
            if cont == 600: cont = 0
            self.janela.update_idletasks()
            self.janela.update()
            # Os updates online são trocados.
            if opcao >= 3:
                self.arquivo() # Salva um arquivo
                response = internet.enviaDados()
                if response.isnumeric():
                    for i in self.players:
                        if i.nome == "Jogador " + "0" + str(int(response) + 3):
                            i.deleta()
                            self.players.remove(i)
                            break
                novas = internet.getAtualizacoes() # É aqui que tem que remover...
                if novas != None and novas != "DELETEALL":
                    ruins = []
                    for i in self.players:
                        nome = i.nome.split()
                        if nome[0] == "Jogador" and int(nome[1]) > 2:
                            pos = int(nome[1])-3
                            if novas[pos] == 'left':
                                i.esquerda()
                            elif novas[pos] == 'right':
                                i.direita()
                            elif novas[pos] == 'up':
                                i.cima()
                            elif novas[pos] == 'down':
                                i.baixo()
                            elif novas[pos] == 'SAIR':
                                i.deleta()
                                ruins.append(i)
                    for i in ruins:
                        self.players.remove(i)
                elif novas == "DELETEALL":
                    ruins = []
                    for i in range(len(self.players)):
                        if self.players[i].nome.split()[0] == "Jogador" and self.players[i].nome not in ["Jogador 01", "Jogador 02"]:
                            self.players[i].deleta()
                            ruins.append(i)
                    ruins.sort(reverse = True)
                    for i in ruins:
                        self.players.pop(i)
                    opcao = opcao - 2
            if auto == 's': # Pra ele andar sozinho
                if opcao >= 1 and jogador.vida > 0:
                    if jogador.movimentos[2]: jogador.esquerda()
                    elif jogador.movimentos[3]: jogador.direita()
                    elif jogador.movimentos[0]: jogador.cima()
                    elif jogador.movimentos[1]: jogador.baixo()
                if opcao in [2, 4] and jogador2.vida > 0:
                    if jogador2.movimentos[2]: jogador2.esquerda()
                    elif jogador2.movimentos[3]: jogador2.direita()
                    elif jogador2.movimentos[0]: jogador2.cima()
                    elif jogador2.movimentos[1]: jogador2.baixo()
            for i in self.players: # Os NPC's Andarem
                i.npc(self.objetos)
            random.shuffle(self.players)
            self.igual(self.players) # Dano nos jogadores
            self.igual2(self.players, powerups) # Pegar os PowerUps
            time.sleep(velocidade)
            if len(self.players) < 2:
                if opcao >= 3:
                    self.arquivo()
                    internet.enviaDados()
                break
        messagebox.showinfo("Fim de Jogo", self.players[0].nome+' venceu o jogo!' )
        ganhador = self.players[0].__dict__
        lista = ["vida", "ataque", "defesa", "nivel", "gloria", "total"]
        print("Informações de", ganhador["nome"])
        for i in lista:
            print(i,":",ganhador[i])
        self.sair()
    
    def arquivo(self):
        resultado = {}
        lista = []
        for i in self.objetos['pl']:
            lista.append(i.json())
        resultado['players'] = lista
        lista = []
        for i in self.objetos['pw']:
            lista.append(i.json())
        resultado['powerups'] = lista
        produto = json.dumps(resultado) # {'players':[], 'powerups':[]}
        arquivo = open('dados.json', 'w')
        arquivo.write(produto)
        arquivo.close()


    def sair(self):
        '''
        Encerra a aplicação
        Funcionamento:
            1 - Quebra o loop.
            2 - Destroi a janela.
        '''
        self.verificador = False #1
        self.janela.destroy()    #2
    
    def atualiza(self):
        '''
        Método para atualizar os scores.

        Funcionamento:
            1 - Tudo é deletado.
            2 - A lista de jogadores é ordenada.
            3 - Cada jogador é adicionado nas tabelas.
        '''
        #1
        self.pn.delete(0, END)
        self.pp.delete(0, END)
        self.pa.delete(0, END)
        self.pd.delete(0, END)
        #2
        self.players.sort(reverse=True)
        #3
        for i in self.players:
            self.pn.insert(END, (i.nome, i.nivel)) # Olhar antes do loop.
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
        result = dfs - atk
        if result != 1:
            atk.listaNegra.append(dfs.id)
        if result == 2:
            atk - dfs
        result = atk - dfs
        if result != 1:
            dfs.listaNegra.append(atk.id)
        if result == 2:
            dfs - atk
        dfs.canvas.itemconfigure(dfs.life, text=str(dfs.vida))
        atk.canvas.itemconfigure(atk.life, text=str(atk.vida))
        #print(atk.nome+":",atk.vida)
        #print(dfs.nome+":",dfs.vida)
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

    def igual(self, locais): # SUBSTITUIR POR canvas.find_overlapping(*canvas.bbox(locais[a].id))
        for a in range(len(locais)):
            for i in range(a+1,len(locais)):
                if i < len(locais) and a < len(locais):
                    if self.compara(locais[a].posicao(), locais[i].posicao()):
                        self.dano(locais[a], locais[i])
    
    def igual2(self, jogadores, objetos):
        for a in range(len(jogadores)):
            for i in objetos:
                if self.compara(jogadores[a].posicao(), i.posicao()):
                    jogadores[a].canvas.itemconfigure(jogadores[a].life, text=str(jogadores[a].vida))
                    jogadores[a] + i
                    i.deleta()
                    objetos.remove(i)
                    del i

class Client:
    def __init__(self, id, servidor):
        self.servidor = servidor
        self.verificador = True
        self.janela = Tk()
        self.janela.title("A abolição do homem.")
        
        self.janela.resizable(0,0)
        self.janela.wm_attributes("-topmost", 1)

        fram = Frame(self.janela)
        tela = Canvas(fram, width=1280, height=700, bd=0, highlightthickness=0)
        pontos = Frame(fram, height=700)
        lb = Label(pontos, text="Pontuação", font="Georgia 20 bold")
        frame = Frame(self.janela)
        vaza = Button(frame, text="Sair!", command=self.sair)

        fram.pack()
        tela.pack(side=LEFT)
        pontos.pack(side=RIGHT)
        lb.pack()
        frame.pack()
        vaza.pack(side='left')

        tela.bind_all("<KeyPress-Left>", self.esquerda)
        tela.bind_all("<KeyPress-Right>", self.direita)
        tela.bind_all("<KeyPress-Up>", self.cima)
        tela.bind_all("<KeyPress-Down>", self.baixo)
        tela.bind_all("<Control_R>", self.para)
        self.direcao = "FAIL"

        # Configurando o jogo
        servidor.atualizaDados()
        informacoes = self.dados()

        self.pn = Multilist(pontos, 9, (("Nome", 15), ("Nível", 1)))
        self.pp = Multilist(pontos, 9, (("Nome", 15), ("Pontos", 1)))
        self.pa = Multilist(pontos, 9, (("Nome", 15), ("Ataque", 1)))
        self.pd = Multilist(pontos, 9, (("Nome", 15), ("Defesa", 1)))
        self.pp.pack(expand=YES, fill=BOTH)
        self.pn.pack(expand=YES, fill=BOTH)
        self.pa.pack(expand=YES, fill=BOTH)
        self.pd.pack(expand=YES, fill=BOTH)
        # Início
        cont = 0
        while self.verificador:
            cont += 1
            try:
                arquivo = open('dados.json', 'r')
                antigo = arquivo.read()
                arquivo.close()
            except:
                antigo = "{}"
            servidor.atualizaDados() # Recebe os dados
            servidor.responder(self.direcao.encode(), servidor.addresses[0]) # Enviando o local.
            informacoes = self.dados() # Decodifica eles
            try:
                antigo = json.loads(antigo)
            except:
                antigo = {}
            if antigo != informacoes:
                if informacoes != {}:
                    if cont == 0 or cont % 200 == 0:
                        self.atualiza(informacoes['players'])
                    tela.delete('all')
                    for i in informacoes['players']:
                        id = tela.create_oval(*i['posicao'], fill = i['cor'])
                        tela.create_text(i['posicao'][0] + 8, i['posicao'][1] - 9, text = i['nome'])
                        tela.create_text(i['posicao'][0] + 8, i['posicao'][1] + 23, text = i['vida'])
                    for i in informacoes['powerups']:
                        id = tela.create_oval(*i['posicao'], fill = i['cor'])
                    if len(informacoes['players']) == 1:
                        messagebox.showinfo("Fim de Jogo", informacoes['players'][0]['nome']+' venceu o jogo!' )
                        self.verificador = False
            self.janela.update_idletasks()
            self.janela.update()
        self.janela.destroy()
        exit()

    def esquerda(self, e): self.direcao = 'left'
    def direita(self, e): self.direcao = 'right'
    def cima(self, e): self.direcao = 'up'
    def baixo(self, e): self.direcao = 'down'
    def para(self, e): self.direcao = 'FAIL'

    def dados(self):
        '''
        Método para ler o arquivo de configurações

        Funcionamento:
            1 - Abre o arquivo json (chamado 'dados.json')
            2 - Decodifica de String para python
        '''
        try:
            arquivo = open('dados.json', 'r') #1
            dados = arquivo.read()
            dados = json.loads(dados) #2
            arquivo.close()
            return dados
        except:
            return {}        

    def atualiza(self, jogadores):
        '''
        Método para atualizar os scores.

        Funcionamento:
            1 - Tudo é deletado.
            2 - Cada jogador é adicionado nas tabelas.
        '''
        #1
        self.pn.delete(0, END)
        self.pp.delete(0, END)
        self.pa.delete(0, END)
        self.pd.delete(0, END)
        #2
        for i in jogadores:
            self.pn.insert(END, (i['nome'], i['nivel'])) 
            self.pp.insert(END, (i['nome'], i['pontos']))
            self.pa.insert(END, (i['nome'], i['ataque']))
            self.pd.insert(END, (i['nome'], i['defesa']))
    
    def sair(self):
        '''
        Método para enviar uma requisição de saída para o servidor.

        Funcionamento:
            1 - Envia a requisição.
            2 - Fecha o socket.
            3 - Destrói a janela.
        '''
        self.servidor.responder("SAIR", self.servidor.addresses[0]) #1
        self.servidor.servidor.close() #2
        messagebox.showinfo("CONEXAO", "Fechando conexão...")
        self.janela.destroy() #3
        exit()
