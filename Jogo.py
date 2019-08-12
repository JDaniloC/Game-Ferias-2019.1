from Objetos import *

def sair(verificador, janela):
    verificador = False
    janela.destroy()
    
def atualiza(pn, pp, pa, pd, players):
    pn.delete(0, END)
    pp.delete(0, END)
    pa.delete(0, END)
    pd.delete(0, END)
    players.sort(reverse=True)
    for i in players:
        pn.insert(END, (i.nome, i.nivel))
        pp.insert(END, (i.nome, i.pontos))
        pa.insert(END, (i.nome, i.ataque))
        pd.insert(END, (i.nome, i.defesa))

def compara(l1, l2):
    if l1[0] <= l2[0]:
        if l1[1] <= l2[1]:
            if l1[2] >= l2[2]:
                if l1[3] >= l2[3]:
                    return True
    return False
    
def dano(atk, dfs, players):
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
    print(atk.nome+":",atk.vida)
    print(dfs.nome+":",dfs.vida)
    try:
        if atk.vida < 1:
            dfs + Xp()
            dfs + Supply()
            atk.deleta()
            players.remove(atk)
            del atk
        if dfs.vida < 1:
            atk + Xp()
            atk + Supply()
            dfs.deleta()
            players.remove(dfs)
            del dfs
    except:
        print("Deu erro!")

def igual(locais): # Antes era recursivo e chegava ao máximo
    for a in range(len(locais)):
        for i in range(a+1,len(locais)):
            if i < len(locais) and a < len(locais):
                if locais[a].posicao() == locais[i].posicao():
                    dano(locais[a], locais[i], locais)

def igual2(jogadores, objetos):
    for a in range(len(jogadores)):
        for i in objetos:
            if compara(jogadores[a].posicao(), i.posicao()):
                jogadores[a].canvas.itemconfigure(jogadores[a].life, text=str(jogadores[a].vida))
                jogadores[a] + i
                i.deleta()
                objetos.remove(i)
                del i

tupla = config().resultado
jogadores, mobs, opcao, frequencia, velocidade, auto = tupla

verificador = True
janela = Tk()
janela.title("A abolição do homem")

janela.resizable(0,0)
janela.wm_attributes("-topmost", 1)

fram = Frame(janela)
tela = Canvas(fram, width=1280, height=700, bd=0, highlightthickness=0)
pontos = Frame(fram, height=700)
lb = Label(pontos, text="Pontuação", font="Georgia 20 bold")
frame = Frame(janela)
botao = Button(frame, text="Pausa!", command=lambda: time.sleep(30))
vaza = Button(frame, text="Sair!", command=partial(sair, verificador, janela))
fram.pack()
tela.pack(side=LEFT)
pontos.pack(side=RIGHT)
lb.pack()
frame.pack()
botao.pack(side="left")
vaza.pack(side='left')

cores = ['navy', 'cornflower blue', 'dark slate blue', 'light sea green', 'lawn green', 'lime green', 'dark khaki', 'goldenrod',  'rosy brown','indian red', 'saddle brown', 'dark orange', 'red', 'hot pink', 'pale violet red', 'maroon', 'snow4', 'SlateBlue1', 'DeepSkyBlue2', 'turquoise1', 'SeaGreen1', 'OliveDrab1']

players = []
powerups = []

if opcao  == 1:
    if auto == 's':
        jogador = Mob(tela, 'blue', "Jogador", 's')
        players.append(jogador)
    else:
        players.append(Mob(tela, 'blue', "Jogador"))
elif opcao == 2:
    if auto == 's':
        jogador = Mob(tela, 'blue', "Jogador", 's')
        jogador2 = Mob(tela, 'green', "Jogador 02", 's')
        players.append(jogador)
        players.append(jogador2)
    else:
        players.append(Mob(tela, 'blue', "Jogador"))
        players.append(Mob(tela, 'green', "Jogador 02"))
        
for i in range(jogadores):
    players.append(Mob(tela, cores[i], cores[i]))
for i in range(mobs):
    powerups.append(Ob(tela))
    powerups.append(Ob2(tela))

objetos = {'pl':players, 'pw':powerups}
cont = 0
pn = Multilist(pontos, 9, (("Nome", 15), ("Nível", 1)))
pp = Multilist(pontos, 9, (("Nome", 15), ("Pontos", 1)))
pa = Multilist(pontos, 9, (("Nome", 15), ("Ataque", 1)))
pd = Multilist(pontos, 9, (("Nome", 15), ("Defesa", 1)))
atualiza(pn, pp, pa, pd, players)
pp.pack(expand=YES, fill=BOTH)
pn.pack(expand=YES, fill=BOTH)
pa.pack(expand=YES, fill=BOTH)
pd.pack(expand=YES, fill=BOTH)

while verificador:
    cont += 1
    if cont % (100*frequencia) == 0:
        powerups.append(Ob(tela))
        powerups.append(Ob2(tela))
    if cont % 300 == 0:
        atualiza(pn, pp, pa, pd, players)
        for i in players:
            i.listaNegra = []
    if cont == 600: cont = 0
    janela.update_idletasks()
    janela.update()
    if auto == 's':
        if opcao >= 1 and jogador.vida > 0:
            if jogador.movimentos[2]: jogador.esquerda()
            elif jogador.movimentos[3]: jogador.direita()
            elif jogador.movimentos[0]: jogador.cima()
            elif jogador.movimentos[1]: jogador.baixo()
        if opcao == 2 and jogador2.vida > 0:
            if jogador2.movimentos[2]: jogador2.esquerda()
            elif jogador2.movimentos[3]: jogador2.direita()
            elif jogador2.movimentos[0]: jogador2.cima()
            elif jogador2.movimentos[1]: jogador2.baixo()
    else:
        if opcao >= 1:
            for i in players:
                if i.id == 1 or i.id == 2:
                    if i.movimentos[2]: jogador.esquerda()
                    elif i.movimentos[3]: jogador.direita()
                    elif i.movimentos[0]: jogador.cima()
                    elif i.movimentos[1]: jogador.baixo()
    for i in players:
        i.npc(objetos)
    random.shuffle(players)
    igual(players)
    igual2(players, powerups)
    time.sleep(velocidade)
    if len(players) < 2:
        break
messagebox.showinfo("Fim de Jogo", players[0].nome+' venceu o jogo!' )
ganhador = players[0].__dict__
lista = ["vida", "ataque", "defesa", "nivel", "gloria", "total"]
print("Informações de", ganhador["nome"])
for i in lista:
    print(i,":",ganhador[i])
sair(verificador, janela)
       
