
# 🤖 Robô de Resgate em Labirinto

Este projeto implementa o software embarcado de um **robô de resgate autônomo** que navega em labirintos para encontrar e salvar humanos perdidos. O robô utiliza sensores para evitar obstáculos, localizar o humano, e retornar com ele para a saída de forma eficiente.

---

## 🛠️ Funcionalidades

- **🚶‍♂️ Navegação Autônoma:** O robô é capaz de se mover em um labirinto, usando comandos simples (avançar, girar, pegar humano, ejetar humano).
- **📡 Sensores:** O robô possui sensores em três direções (esquerda, frente, e direita) para detectar paredes, espaço livre, e o humano.
- **🔄 Labirinto Randomizado:** O ambiente do labirinto pode ser gerado de forma aleatória a cada simulação, garantindo testes em diferentes cenários.
- **📝 Registro de Operações:** Cada movimento e leitura dos sensores é registrado em um arquivo de log CSV para auditoria.
- **✅ Casos de Teste:** Um conjunto de testes unitários foi desenvolvido para garantir a robustez das funcionalidades do robô e a operação em diferentes ambientes.

---

## 📂 Estrutura do Projeto

```bash
/projeto_robo_resgate
├── /logs/                      # Logs gerados durante a execução do programa
├── robo_resgate.py              # Classe principal do robô de resgate
├── testes.py                    # Arquivo de testes unitários
└── main.py                      # Script principal para simulação
```

## Como Executar

### Importante: 

Esse codigo tem como modelo visual o uso da lib (`pygame`), faça a instalação de maneira correta dentro do projeto após baixar o repositorio: 
```bash
pip install pygame
```

### Simulação de Labirinto Randomizado

Essa Funcionalidade Foi implementada automaticamente no codigo , por tanto cada labririnto quando rodamos e diferente: 
```bash
python main.py
```




Isso irá criar um labirinto, colocar o robô na entrada, executar uma sequência de comandos, e salvar os logs em um arquivo CSV (`log_resgate.csv`).

### Testes Unitários

Para rodar os testes unitários e validar o comportamento do robô, execute:

```bash
python testes.py
```

## Exemplos de Uso

1. O robô começa em uma posição inicial na entrada do labirinto e explora o ambiente em busca de um humano perdido.
2. O labirinto é gerado aleatoriamente em cada execução, tornando o ambiente de teste variado.

3. Após encontrar o humano, o robô retorna com segurança para a saída e ejeta o humano.

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou novos casos de teste! Basta abrir uma **issue** ou enviar um **pull request**.

## Alunos Responsaveis pelo projeto :
.Daniel Filipe Tavares Rodrigues RA:2022101144 

.Nathan Moraes Corrêa RA:2022101394

.Matheus Henrique De Lima Batista RA:2021103836  

.Yan Percegona Weiss RA: 2022101667
