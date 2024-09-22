import os

class RoboResgate:
    def __init__(self, labirinto, nome_arquivo):
        self.labirinto = labirinto
        self.posicao = self.encontrar_entrada()
        self.direcao = 'L'  # Direção inicial para o Leste
        self.encontrou_humano = False
        self.carregando_humano = False
        self.ordem_direcoes = ['L', 'N', 'O', 'S']  # Ordem de tentativas de movimento
        self.visitadas = set()  # Conjunto de posições visitadas
        self.caminho = []  # Pilha para armazenar o caminho percorrido
        self.log_movimentos = []  # Lista para registrar todos os movimentos feitos
        self.visitadas.add(self.posicao)  # Marca a posição inicial como visitada
        self.caminho.append(self.posicao)  # Adiciona a posição inicial ao caminho
        self.nome_arquivo_log = nome_arquivo  # Nome do arquivo de log (mapa + extensão .csv)

        # Log inicial ao ligar o robô
        self.log_movimento("LIGAR", *self.sensores(), "SEM CARGA")

    def encontrar_entrada(self):
        # Procura a entrada 'E' no labirinto
        for y, linha in enumerate(self.labirinto.mapa):
            for x, celula in enumerate(linha):
                if celula == 'E':
                    return (x, y)
        return (0, 0)  # Fallback

    def sensores(self):
        """Retorna as leituras dos sensores (esquerda, frente, direita)"""
        esquerda = self.verificar_sensor(self.direcao_esquerda())
        frente = self.verificar_sensor(self.direcao)
        direita = self.verificar_sensor(self.direcao_direita())
        return esquerda, frente, direita

    def verificar_sensor(self, direcao):
        """Verifica o que há na célula adjacente na direção fornecida."""
        movimentos = {
            'N': (0, -1),
            'S': (0, 1),
            'L': (1, 0),
            'O': (-1, 0)
        }
        dx, dy = movimentos[direcao]
        nova_posicao = (self.posicao[0] + dx, self.posicao[1] + dy)

        # Verifica os limites do labirinto
        if not (0 <= nova_posicao[1] < len(self.labirinto.mapa) and
                0 <= nova_posicao[0] < len(self.labirinto.mapa[0])):
            return 'PAREDE'

        # Verifica o conteúdo da célula
        celula = self.labirinto.mapa[nova_posicao[1]][nova_posicao[0]]
        if celula == '*':
            return 'PAREDE'
        elif celula == 'H':
            return 'HUMANO'
        else:
            return 'VAZIO'

    def direcao_esquerda(self):
        """Retorna a direção à esquerda do robô."""
        indice = self.ordem_direcoes.index(self.direcao)
        return self.ordem_direcoes[(indice - 1) % 4]

    def direcao_direita(self):
        """Retorna a direção à direita do robô."""
        indice = self.ordem_direcoes.index(self.direcao)
        return self.ordem_direcoes[(indice + 1) % 4]

    def avancar(self):
        """Comando A: Avança o robô uma posição."""
        _, frente, _ = self.sensores()
        if frente == 'VAZIO':
            self.mover(self.direcao)
            self.log_movimento("A", *self.sensores())
        elif frente == 'HUMANO':
            # Se o humano estiver à frente, o robô para e tenta pegar o humano
            print("Humano detectado à frente!")
            self.pegar_humano()
        else:
            print("Alarme: Tentativa de colidir com", frente)  # Alarme de colisão com parede
            self.log_movimento("ALARME_COLISAO", *self.sensores(), "ERRO: PAREDE")

    def girar_direita(self):
        """Comando G: Gira o robô 90 graus à direita."""
        indice = self.ordem_direcoes.index(self.direcao)
        self.direcao = self.ordem_direcoes[(indice + 1) % 4]
        self.log_movimento("G", *self.sensores())

    def pegar_humano(self):
        """Comando P: Tenta pegar o humano à frente."""
        _, frente, _ = self.sensores()
        if frente == 'HUMANO':
            self.carregando_humano = True
            self.log_movimento("P", *self.sensores(), "COM HUMANO")
            print("Humano resgatado com sucesso!")
        else:   # Alarme de coleta sem humano
                print("Alarme: Tentativa de coleta sem humano à frente!") 
                self.log_movimento("ALARME_COLETA", *self.sensores(), "ERRO: SEM HUMANO") 

    def ejetar_humano(self):
        """Comando E: Ejeta o humano fora do labirinto."""
        if self.carregando_humano and self.esta_na_saida():
            self.carregando_humano = False
            self.log_movimento("E", *self.sensores(), "SEM CARGA")
            print("Humano ejetado com sucesso!")
        else: # Alarme de ejeção sem humano
            print("Alarme: Tentativa de ejeção sem humano!") 
            self.log_movimento("ALARME_EJECAO", *self.sensores(), "ERRO: SEM HUMANO OU NAO ESTA NA SAIDA")

    def esta_na_saida(self):
        """Verifica se o robô está na saída e de frente para fora do labirinto."""
        _, frente, _ = self.sensores()
        # Verifica se está na entrada e de frente para o vazio (saída)
        return self.posicao == self.encontrar_entrada() and frente == 'VAZIO'

    def mover(self, direcao):
        """Move o robô em uma direção específica."""
        movimentos = {
            'N': (0, -1),
            'S': (0, 1),
            'L': (1, 0),
            'O': (-1, 0)
        }
        dx, dy = movimentos[direcao]
        nova_posicao = (self.posicao[0] + dx, self.posicao[1] + dy)

        # Verifica se a nova posição está dentro dos limites
        if 0 <= nova_posicao[1] < len(self.labirinto.mapa) and 0 <= nova_posicao[0] < len(self.labirinto.mapa[0]):
            # Verifica se pode mover
            if self.labirinto.mapa[nova_posicao[1]][nova_posicao[0]] != '*':
                self.posicao = nova_posicao
                self.visitadas.add(nova_posicao)
                self.caminho.append(self.posicao)


    def mover_auto(self):
        """Movimenta o robô de forma autônoma, priorizando direções não visitadas"""
        if not self.encontrou_humano:
            # Verifica as direções possíveis e escolhe a primeira não visitada
            for direcao in self.ordem_direcoes:
                if self.pode_mover(direcao) and not self.posicao_ja_visitada(direcao):
                    self.direcao = direcao
                    self.mover(self.direcao)
                    self.log_movimento("MOV_AUTO", *self.sensores(), "COM HUMANO" if self.carregando_humano else "SEM CARGA")
                    self.verificar_humano()
                    return

            # Se todas as direções foram visitadas, faz o backtracking
            self.fazer_backtracking()

        elif self.carregando_humano and not self.esta_na_saida():
            # Verifica as direções possíveis para retornar à entrada
            for direcao in self.ordem_direcoes:
                if self.pode_mover(direcao):
                    self.direcao = direcao
                    self.mover(self.direcao)
                    # Log de movimento com humano durante o retorno
                    self.log_movimento("MOV_RETORNO", *self.sensores(), "COM HUMANO")
                    return

        # Se estiver na saída, ejeta o humano
        if self.carregando_humano and self.esta_na_saida():
            self.ejetar_humano()
            # Adicionando log ao ejetar o humano
            self.log_movimento("E", *self.sensores(), "EJETA HUMANO, ROBO SEM CARGA")

            # Se todas as direções foram visitadas, faz o backtracking
            self.fazer_backtracking()

        elif self.encontrou_humano and not self.esta_na_saida():
            # Verifica as direções possíveis para retornar à entrada
            for direcao in self.ordem_direcoes:
                if self.pode_mover(direcao):
                    self.direcao = direcao
                    self.mover(self.direcao)
                    self.log_movimento("MOV_RETORNO", *self.sensores())  # Log de movimento com humano
                    return

    def pode_mover(self, direcao):
        """Verifica se o robô pode se mover em uma direção"""
        movimentos = {
            'N': (0, -1),
            'S': (0, 1),
            'L': (1, 0),
            'O': (-1, 0)
        }
        dx, dy = movimentos[direcao]
        nova_posicao = (self.posicao[0] + dx, self.posicao[1] + dy)

        # Verifica se a nova posição está dentro dos limites do labirinto
        if not (0 <= nova_posicao[1] < len(self.labirinto.mapa) and
                0 <= nova_posicao[0] < len(self.labirinto.mapa[0])):
            return False

        # Verifica se há parede
        return self.labirinto.mapa[nova_posicao[1]][nova_posicao[0]] != '*'

    def verificar_humano(self):
        """Verifica se o humano está à frente"""
        _, frente, _ = self.sensores()
        if frente == 'HUMANO':
            self.pegar_humano()

    def posicao_ja_visitada(self, direcao):
        """Verifica se a nova posição na direção especificada já foi visitada."""
        movimentos = {
            'N': (0, -1),
            'S': (0, 1),
            'L': (1, 0),
            'O': (-1, 0)
        }
        dx, dy = movimentos[direcao]
        nova_posicao = (self.posicao[0] + dx, self.posicao[1] + dy)

        # Retorna True se a nova posição já foi visitada
        return nova_posicao in self.visitadas

    def fazer_backtracking(self):
        """Faz o robô retroceder no caminho quando necessário"""
        if len(self.caminho) > 1:
            self.caminho.pop()  # Remove a posição atual (beco sem saída)
            self.posicao = self.caminho[-1]  # Volta para a posição anterior
            self.log_movimento("BACKTRACK", *self.sensores())  # Log de movimento no backtracking
            if self.carregando_humano: # Alarme de beco sem saída após coleta
                print("Alarme: Beco sem saída após coletar humano!")  
                self.log_movimento("ALARME_BECO", *self.sensores(), "ERRO: BECO COM HUMANO")

    def log_movimento(self, comando, esquerda, frente, direita, carga=None):
   
        if carga is None:
            carga = "COM HUMANO" if self.carregando_humano else "SEM CARGA"
    
        linha_log = f"{comando},{self.posicao[0]},{self.posicao[1]},{esquerda},{frente},{direita},{carga}"
        self.log_movimentos.append(linha_log)

    def salvar_log(self):
        """Salva o log de operação em um arquivo CSV."""
        # Define o caminho da pasta de logs
        pasta_logs = "logs"
        # Cria a pasta, se ela não existir
        os.makedirs(pasta_logs, exist_ok=True)
        # Define o caminho completo do arquivo
        caminho_completo = os.path.join(pasta_logs, f"{self.nome_arquivo_log}.csv")

        with open(caminho_completo, 'w') as arquivo_log:
        # Escreve o cabeçalho do log
            arquivo_log.write("Comando,Posicao X,Posicao Y,Sensor Esquerdo,Sensor Frente,Sensor Direito,Carga\n")
            for linha in self.log_movimentos:
                arquivo_log.write(linha + "\n")
