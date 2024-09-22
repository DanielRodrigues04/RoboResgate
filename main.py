from robo.robo_resgate import RoboResgate
from robo.labirinto import Labirinto
from robo.simulador import Simulador

def main():
    largura, altura = 10, 10  # Dimensões do labirinto
    labirinto = Labirinto(largura, altura)  # Gera o labirinto automaticamente
    nome_arquivo_log = "log_resgate"  # Nome do arquivo de log

    # Instancia o RoboResgate, passando o labirinto e o nome do arquivo de log
    robo = RoboResgate(labirinto, nome_arquivo_log)

    simulador = Simulador(labirinto, robo)  # Inicializa o simulador

    simulador.rodar()  # Executa o simulador

    # Salva o log ao final
    robo.salvar_log()

if __name__ == "__main__":
    main()
