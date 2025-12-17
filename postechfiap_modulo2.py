# Imports
from typing import List
from algoritmos_geneticos import populacao_inicial_aleatoria
from draw_functions import draw_cities, draw_paths, draw_plot
from utils import imprimir_matriz, indice_para_letra, ler_inteiro_positivo, limpar_console
import math
import pygame
import random



# Constantes/macros de configuração
MIN_CIDADES = 5
MAX_CIDADES = 15
MIN_POPULACAO = 25
MAX_POPULACAO = 100
LIM_CARRO_ELETRICO = 150

# Constantes/macros de velocidade média dos transportes (em pixels por unidade de tempo)
VELOC_AVIAO = 480
VELOC_TREM = 100
VELOC_CARRO_ELETRICO = 90
VELOC_CAMINHAO = 60

# Constantes/macros de custo médio dos transportes (em R$ por pixel)
CUSTO_AVIAO = 6
CUSTO_TREM = 2
CUSTO_CARRO_ELETRICO = 3
CUSTO_CAMINHAO = 4

# Constantes/macros de configuração do Pygame
LARGURA_TELA = 860
ALTURA_TELA = 460
OFFSET_X_GRAFICO = 400
MARGEM = 30
COR_BRANCO = (255, 255, 255)
COR_VERMELHA = (255, 0, 0)
RAIO = 7
FPS = 30




# Rotina Prncipal
if __name__ == "__main__":

    # Introdução
    limpar_console()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("*                  POS-TECH FIAP - Módulo 02                  *")
    print("*                  IA PARA DEV - TURMA 7IADT                  *")
    print("*  PROJETO 2 - Solução para o problema do Caixeiro Viajante   *")
    print("*            (TSP - Traveling Salesperson Problem)            *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")



    # Definição do número de cidades
    print("1 - DEFINIÇÃO DO NÚMERO DE CIDADES")
    entrada = None
    numCidades: int
    while entrada is None:
        print(f"Digite um número inteiro positivo maior ou igual a {MIN_CIDADES} e menor ou igual a {MAX_CIDADES}: ", end="", flush=True)
        entrada = ler_inteiro_positivo(MIN_CIDADES, MAX_CIDADES)
        if entrada is not None:
            numCidades = entrada
            print(f"Número de cidades definido para {numCidades}.\n")



    # Definindo posicionamento das cidades aleatoriamente
    print("2 - POSICIONAMENTO ALEATÓRIO DAS CIDADES")
    cidades = {
        cidade: posicao
        for cidade, posicao
        in zip(
            [indice_para_letra(i) for i in range(numCidades)],
            [(random.randint(OFFSET_X_GRAFICO + MARGEM, LARGURA_TELA - MARGEM), random.randint(MARGEM, ALTURA_TELA - MARGEM)) for _ in range(numCidades)])}
    print(f"Cidades posicionadas aleatoriamente em um terreno de {LARGURA_TELA - OFFSET_X_GRAFICO - 2 * MARGEM} x {ALTURA_TELA - 2 * MARGEM}:\n{"\n".join(f"{k}: {v}" for k, v in cidades.items())}\n")



    # Calculando a distância euclidiana de cada par de cidades para montar a matriz de distâncias
    print("3 - DEFININDO MATRIZ DE DISTÂNCIAS ENTRE AS CIDADES")
    matrizDistancias = [[0.0 for _ in range(numCidades)] for _ in range(numCidades)]
    for i in range(numCidades):
        xi, yi = cidades[indice_para_letra(i)]
        for j in range(i + 1, numCidades):
            xj, yj = cidades[indice_para_letra(j)]
            d = math.hypot(xi - xj, yi - yj)
            matrizDistancias[i][j] = d
            matrizDistancias[j][i] = d
    print("Matriz de distâncias calculada: \n")
    imprimir_matriz(matrizDistancias)



    # Definindo aleatoriamente rotas possíveis de avião entre as cidades
    print("4 - DEFININDO ALEATORIAMENTE ROTAS UNIDIRECIONAIS POSSÍVEIS DE AVIÃO ENTRE AS CIDADES")
    entrada = None
    perc_cnx_aviao: int
    while entrada is None:
        print(f"Digite um percentual válido entre 0 e 100 para a proporção de rotas possíveis de avião: ", end="", flush=True)
        entrada = ler_inteiro_positivo(0, 100)
        if entrada is not None:
            perc_cnx_aviao = entrada
    qtd_cnx_aviao = (numCidades * (numCidades - 1)) * perc_cnx_aviao // 100
    print(f"Percentual de rotas de avião definido para {perc_cnx_aviao}%, resultando em {qtd_cnx_aviao} rotas unidirecionais possíveis.\n")
    vetor_rotas_aviao = list(range((numCidades * (numCidades - 1))))
    rotas_aviao = sorted(random.sample(vetor_rotas_aviao, k = qtd_cnx_aviao))
    matrizAviao = [[0 for _ in range(numCidades)] for _ in range(numCidades)]
    for rota in rotas_aviao:
        xma = rota // (numCidades - 1)
        yma = rota % (numCidades - 1)
        if yma >= xma:
            yma += 1
        matrizAviao[xma][yma] = 1
    print("Matriz de rotas de avião: \n")
    imprimir_matriz(matrizAviao)



    # Definindo aleatoriamente rotas possíveis de trem entre as cidades
    print("5 - DEFININDO ALEATORIAMENTE ROTAS BIDIRECIONAIS POSSÍVEIS DE TREM ENTRE AS CIDADES")
    entrada = None
    perc_cnx_trem: int
    while entrada is None:
        print(f"Digite um percentual válido entre 0 e 100 para a proporção de rotas possíveis de trem: ", end="", flush=True)
        entrada = ler_inteiro_positivo(0, 100)
        if entrada is not None:
            perc_cnx_trem = entrada
    qtd_cnx_trem = (numCidades * (numCidades - 1) // 2) * perc_cnx_trem // 100
    print(f"Percentual de rotas de trem definido para {perc_cnx_trem}%, resultando em {qtd_cnx_trem} rotas bidirecionais possíveis.\n")
    vetor_rotas_trem = list(range((numCidades * (numCidades - 1) // 2)))
    rotas_trem = sorted(random.sample(vetor_rotas_trem, k = qtd_cnx_trem))
    matrizTrem = [[0 for _ in range(numCidades)] for _ in range(numCidades)]
    ymt, controle = 0, 0
    for rota in rotas_trem:
        while rota >= controle + (numCidades - ymt - 1):
            controle += (numCidades - ymt - 1)
            ymt += 1
        xmt = rota - controle + ymt + 1
        matrizTrem[xmt][ymt] = 1
        matrizTrem[ymt][xmt] = 1
    print("Matriz de rotas de trem: \n")
    imprimir_matriz(matrizTrem)



    # Definição do tamanho da população inicial para o algoritmo genético
    print("6 - DEFINIÇÃO DO TAMANHO DA POPULAÇÃO")
    entrada = None
    tamPopulacao: int
    while entrada is None:
        print(f"Digite um número inteiro positivo maior ou igual a {MIN_POPULACAO} e menor ou igual a {MAX_POPULACAO}: ", end="", flush=True)
        entrada = ler_inteiro_positivo(MIN_POPULACAO, MAX_POPULACAO)
        if entrada is not None:
            tamPopulacao = entrada
            print(f"Tamanho da população definido para {tamPopulacao}.\n")



    # Escolha do algoritmo de geração da população inicial
    print("7 - GERAÇÃO DA POPULAÇÃO INICIAL")
    print("Escolha o algoritmo de geração da população inicial:")
    print("1 - Aleatória")
    entrada = None
    populacao_inicial: List[List[str]]
    while entrada is None:
        print("Algoritmo de geração da população inicial: ", end="", flush=True)
        entrada = ler_inteiro_positivo(1, 1)
        if entrada is not None:
            if entrada == 1:
                teste = list(cidades.keys())
                populacao_inicial = populacao_inicial_aleatoria(teste, tamPopulacao)
            else:
                # Implementar heurística aqui
                pass
    print(f"População inicial gerada com {len(populacao_inicial)} indivíduos:\n{"\n".join(f"{individuo}" for individuo in populacao_inicial)}\n")



    # Inicializando a solução do problema do caixeiro viajante usando algoritmo genético
    input("Pressione ENTER para iniciar a solução do problema do caixeiro viajante usando algoritmo genético...")
    pygame.init()
    pygame.display.set_caption("PÓS TECH FIAP - Turma 7IADT/Módulo 02 - TSP Solver")
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    clock = pygame.time.Clock()

    # Loop de execução
    emExecucao: bool = True
    while emExecucao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                emExecucao = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    emExecucao = False

        tela.fill(COR_BRANCO)
        draw_plot(tela, list(range(10)), list(range(10)), y_label="Gráfico de fitness")
        draw_cities(tela, list(cidades.values()), COR_VERMELHA, RAIO, list(cidades.keys()))
    
        pygame.display.flip()
        clock.tick(FPS)



    # Finalização
    print(f"\n\nFim do módulo \"{__name__}\"\n")
