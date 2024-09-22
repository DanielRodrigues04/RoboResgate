import pygame
import time


class Simulador:
    def __init__(self, labirinto, robo):
        self.labirinto = labirinto
        self.robo = robo
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Simulador do Robô de Resgate")
        self.clock = pygame.time.Clock()
        self.tamanho_celula = 50  # Tamanho de cada célula no labirinto
        self.cor_fundo = (173, 216, 230)  # Azul claro para fundo
        self.fonte = pygame.font.SysFont(None, 40)

    def desenhar_labirinto(self):
        # Desenha o labirinto na tela
        for y, linha in enumerate(self.labirinto.mapa):
            for x, celula in enumerate(linha):
                if celula == '*':
                    cor = (0, 0, 0)  # Preto para paredes
                elif celula == ' ':
                    cor = (255, 255, 255)  # Branco para caminhos
                elif celula == 'E':
                    cor = (0, 0, 255)  # Azul para entrada
                elif celula == 'H':
                    cor = (0, 255, 0)  # Verde para humano

                # Desenha a célula correspondente
                pygame.draw.rect(self.tela, cor, pygame.Rect(
                    x * self.tamanho_celula, y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula))

                # Desenha as siglas (E para entrada e H para humano)
                if celula == 'E':
                    self.desenhar_sigla('E', x, y)
                elif celula == 'H':
                    self.desenhar_sigla('H', x, y)

        # Desenha o robô com uma borda amarela ao redor
        self.desenhar_robo()

    def desenhar_robo(self):
        # Posição atual do robô
        x, y = self.robo.posicao
        # Desenhar a borda amarela
        pygame.draw.rect(self.tela, (255, 255, 0), pygame.Rect(
            x * self.tamanho_celula, y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula), 5)
        # Desenhar o robô no centro da célula
        self.desenhar_sigla('R', x, y)

    def desenhar_sigla(self, letra, x, y):
        # Renderiza as letras (R para robô, E para entrada, H para humano)
        # Cor vermelha para a letra
        texto = self.fonte.render(letra, True, (255, 0, 0))
        self.tela.blit(texto, (x * self.tamanho_celula +
                       10, y * self.tamanho_celula + 5))

    def rodar(self):
        # Inicia o loop principal do simulador com inteligência artificial para mover o robô
        running = True
        humano_resgatado = False
        enquanto_na_saida = False  # Para detectar se o robô chegou à saída com o humano

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Movimenta o robô automaticamente
            if not humano_resgatado:
                self.robo.mover_auto()

            # Preenche a tela com a cor de fundo
            self.tela.fill(self.cor_fundo)
            # Desenha o labirinto com o robô
            self.desenhar_labirinto()
            pygame.display.flip()  # Atualiza a tela
            # Define a taxa de atualização para 5 FPS, para simular o movimento
            self.clock.tick(5)

            # Verifica se o humano foi encontrado e resgatado
            if self.robo.encontrou_humano and not humano_resgatado:
                humano_resgatado = True
                print("Humano encontrado e resgatado! Agora indo para a saída.")

            # Se o humano foi resgatado, o robô deve continuar até a saída
            if humano_resgatado:
                if not self.robo.esta_na_saida():
                    self.robo.mover_auto()  # Continue movendo até a saída
                else:
                    if not enquanto_na_saida:
                        print("Chegou à saída! Ejetando humano...")
                        self.robo.ejetar_humano()
                        enquanto_na_saida = True
                        time.sleep(2)  # Pausa para visualizar a ejeção
                        running = False

        pygame.quit()  # Encerra o pygame ao sair do loop
