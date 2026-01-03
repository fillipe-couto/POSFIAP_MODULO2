# Imports
from algoritmos_geneticos import calcular_fitness_prioridade_tempo, calcular_limites_estimados, edge_recombination_crossover, populacao_inicial_aleatoria, selecao_por_torneio
from draw_functions import draw_cities, draw_paths, draw_plot
from operator import itemgetter
from parametros import ALTURA_TELA, COR_AZUL, COR_BRANCO, FPS, LARGURA_TELA, MARGEM, MAX_CIDADES, MAX_POPULACAO, MIN_CIDADES, MIN_POPULACAO, OFFSET_X_GRAFICO
from utils import imprimir_matriz, indice_para_letra, ler_inteiro_positivo, limpar_console
from typing import List, Tuple
import math
import pygame
import random



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
    numCidades: int = 0
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
    cidades_str = "\n".join(f"{k}: {v}" for k, v in cidades.items())
    print(f"Cidades posicionadas aleatoriamente em um terreno de {LARGURA_TELA - OFFSET_X_GRAFICO - 2 * MARGEM} x {ALTURA_TELA - 2 * MARGEM}:\n{cidades_str}\n")



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
    perc_cnx_aviao: int = 0
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
    perc_cnx_trem: int = 0
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
    tamPopulacao: int = 0
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
    populacao: List[List[str]] = []
    while entrada is None:
        print("Algoritmo de geração da população inicial: ", end="", flush=True)
        entrada = ler_inteiro_positivo(1, 1)
        if entrada is not None:
            if entrada == 1:
                populacao = populacao_inicial_aleatoria(list(cidades.keys()), tamPopulacao)
            else:
                # Implementar heurística aqui
                pass



    # Inicializando a solução do problema do caixeiro viajante usando algoritmo genético
    input("\nPressione ENTER para iniciar a solução do problema do caixeiro viajante usando algoritmo genético...\n")
    pygame.init()
    pygame.display.set_caption("PÓS TECH FIAP - Turma 7IADT/Módulo 02 - TSP Solver")
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    clock = pygame.time.Clock()

    limites_estimados = calcular_limites_estimados(matrizDistancias)
    geracao = 0
    melhores_solucoes: List[Tuple[List[str], float, List[int]]] = []

    # Loop de execução
    emExecucao: bool = True
    while emExecucao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                emExecucao = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    emExecucao = False
        
        geracao += 1
        populacao_fitness_trajeto: List[Tuple[List[str], float, List[int]]] = []
        for individuo in populacao:
            populacao_fitness_trajeto.append(
                calcular_fitness_prioridade_tempo(
                    matrizDistancias,
                    matrizAviao,
                    matrizTrem,
                    individuo,
                    *limites_estimados))
        populacao_fitness_trajeto.sort(key=itemgetter(1), reverse=False)
        melhores_solucoes.append(populacao_fitness_trajeto[0])

        tela.fill(COR_BRANCO)
        draw_plot(tela, list(range(len(melhores_solucoes))), [solucao[1] for solucao in melhores_solucoes], y_label="Gráfico de fitness")
        draw_cities(tela, list(cidades.values()), list(cidades.keys()))
        draw_paths(tela, melhores_solucoes[-1], cidades)
        pygame.display.flip()
        clock.tick(FPS)

        print(f"Geração {geracao}: Fitness {melhores_solucoes[-1][1]:5.3f} - Trajeto {melhores_solucoes[-1][0]}, Transportes {melhores_solucoes[-1][2]}\r", end="", flush=True)
        
        # ------------------------------------------------------------
        # Implementação do algoritmo genético: seleção
        # ------------------------------------------------------------

        # Elitismo: definindo a nova população inicial com os 10% melhores
        nova_populacao: List[List[str]] = list(populacao_fitness_trajeto[i][0] for i in range(tamPopulacao // 10))

        # ------------------------------------------------------------
        # Implementação do algoritmo genético: cruzamento
        # - Utiliza toneiro para selecionar os pais;
        # - Utiliza Edge Recombination Crossover (ERX) para gerar os filhos;
        # ------------------------------------------------------------
        while len(nova_populacao) < tamPopulacao:
            nova_populacao.extend(
                edge_recombination_crossover(
                    selecao_por_torneio(populacao_fitness_trajeto),
                    selecao_por_torneio(populacao_fitness_trajeto)))
        
        # Finalizando esta geração, definindo a população para a próxima geração
        populacao = nova_populacao[:tamPopulacao]        

    # Finalização
    print(f"\n\nFim do módulo \"{__name__}\"\n")
