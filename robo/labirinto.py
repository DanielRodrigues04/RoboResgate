import random

class Labirinto:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.mapa = self.gerar_labirinto()

    def gerar_labirinto(self):
        # Inicializa o labirinto todo com paredes
        mapa = [['*' for _ in range(self.largura)] for _ in range(self.altura)]

        # Algoritmo DFS para criar caminhos no labirinto
        def criar_caminho(x, y):
            direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Baixo, Direita, Cima, Esquerda
            random.shuffle(direcoes)  # Embaralha as direções para aleatoriedade

            for dx, dy in direcoes:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 1 <= nx < self.largura - 1 and 1 <= ny < self.altura - 1:
                    if mapa[ny][nx] == '*':
                        mapa[ny][nx] = ' '
                        mapa[ny - dy][nx - dx] = ' '
                        criar_caminho(nx, ny)

        # Começa no ponto (1, 1)
        mapa[1][1] = ' '
        criar_caminho(1, 1)

        # Posiciona a entrada (E) e o humano (H) no labirinto
        mapa[1][0] = 'E'  # Entrada na posição esquerda

        # Gera uma posição aleatória dentro do labirinto para o humano (evitando bordas)
        humano_pos = (random.randint(1, self.largura - 2), random.randint(1, self.altura - 2))
        while mapa[humano_pos[1]][humano_pos[0]] != ' ':  # Garante que o humano fique em um caminho vazio
            humano_pos = (random.randint(1, self.largura - 2), random.randint(1, self.altura - 2))
        hx, hy = humano_pos
        mapa[hy][hx] = 'H'  # Define a posição do humano

        return mapa
