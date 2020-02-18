from socket import *

class Internet:
    def __init__(self, port = None):
        '''
        Objeto para ocorrer o jogo multiplayer

        port - A porta do socket
        '''
        self.servidor = socket(AF_INET, SOCK_DGRAM)
        if port != None:
            self.servidor.bind(('', port))
        self.servidor.settimeout(1.0)
        self.addresses = [] # Os endereços devem ficar aqui.
        self.id = None

    def conectarClient(self, ip, port):
        '''
        Onde o client requisita o servidor.
        '''
        try:
            if self.addresses == []:
                self.servidor.sendto(b"CONNECT", (ip, port))
            self.servidor.settimeout(5)
            self.id = self.receber().decode()
            self.servidor.settimeout(1)
            self.addresses.append((ip, port))
            return "OK"
        except Exception as e:
            print(e)
            return "FAIL"

    def conectarServidor(self):
        '''
        Onde o servidor recebe todos as requisições de conexão.
        '''
        try:
            mensagem, address = self.servidor.recvfrom(2048)
            while mensagem == b"CONNECT":
                self.addresses.append(address)
                cont = 0
                response = self.responder(str(len(self.addresses)).encode(), address)
                while cont < 3 and response != "OK":
                    response = self.responder(str(len(self.addresses)).encode(), address)
                    cont += 1
                if cont == 3: self.addresses.pop(len(self.addresses) - 1)
                mensagem, address = self.servidor.recvfrom(2048)
            return "OK"
        except Exception as e:
            print(e)
            return "FAIL"

    def atualizaDados(self):
        '''
        Onde o client recebe os novos updates.
        '''
        dados = open('dados.json', 'wb')
        mensagem = self.receber()
        while mensagem != "FAIL" and mensagem != b"OK":
            dados.write(mensagem)
            mensagem = self.receber()
        dados.close() 

    def enviaDados(self):
        '''
        Onde ele repassa todas as informações para todos os clientes.
        '''
        try:
            # Cria toada as partes para serem enviadas.
            resultado = "OK"
            dados = open('dados.json', 'rb')
            conteudo = []
            parte = dados.read(2048)
            while parte:
                conteudo.append(parte)
                parte = dados.read(2048)

            # Envia para cada um deles.            
            for client in self.addresses:
                if client != None:
                    cont = 0
                    for parte in conteudo:
                        response = self.responder(parte, client)
                        if response == "FAIL":
                            while cont < 3 and response == "FAIL":
                                response = self.responder(parte, client)
                                cont += 1
                            if cont == 3: 
                                resultado = str(self.addresses.index(client))
                                self.addresses[self.addresses.index(client)] = None
                    self.responder(b"OK", client)
            dados.close()
            return resultado
        except Exception as e:
            print(e)
            return "FAIL"

    def getAtualizacoes(self):
        '''
        Recebe as novas posições se houver
        '''
        #self.servidor.settimeout(0.2)
        lista = ["FAIL" for x in self.addresses]
        cont = len(lista)
        while cont > 0:
            try:
                mensagem, endereco = self.servidor.recvfrom(2048)
                for i in range(len(self.addresses)):
                    if endereco == self.addresses[i]:
                        if mensagem.decode() == "SAIR":
                            self.addresses[i] = None
                        lista[i] = mensagem.decode()
                        cont -= 1
                    elif self.addresses[i] == None:
                        cont -= 1
            except ConnectionResetError: # Significa que não tem ninguém conectado...
                return "DELETEALL"
            except Exception as e:
                print(e)
                cont -= 1
        
        return lista

    def receber(self):
        '''
        Comando básico de receber os dados, para não devolver exceção.
        '''
        try:
            mensagem, endereco = self.servidor.recvfrom(2048)
        except Exception as e:
            print(e)
            mensagem = "FAIL"
        return mensagem

    def responder(self, dados, endereco):
        '''
        Comando básico para enviar dados, para não devolver exceção.
        '''
        try:
            self.servidor.sendto(dados, endereco)
            resultado = "OK"
        except Exception as e:
            print(e)
            resultado = "FAIL"
        return resultado

    def __len__(self): return len(self.addresses)
    
