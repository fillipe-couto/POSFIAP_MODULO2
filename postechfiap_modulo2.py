# Imports
import math
import os
import random
import time
from operator import itemgetter
from typing import List, Tuple

import pygame

from algoritmos_geneticos import (
    aplicar_mutacoes,
    calcular_fitness_prioridade_tempo,
    calcular_limites_estimados,
    edge_recombination_crossover,
    populacao_inicial_aleatoria,
    selecao_por_torneio,
)
from draw_functions import draw_cities, draw_paths, draw_plot
from parametros import (
    ALTURA_TELA,
    COR_BRANCO,
    FPS,
    LARGURA_TELA,
    MARGEM,
    MAX_CIDADES,
    MAX_GERACOES_SEM_MELHORIA,
    MAX_MAX_GERACOES,
    MAX_POPULACAO,
    MIN_CIDADES,
    MIN_GERACOES_SEM_MELHORIA,
    MIN_MAX_GERACOES,
    MIN_POPULACAO,
    OFFSET_X_GRAFICO,
)
from relatorio import gerar_relatorio_pdf
from utils import (
    imprimir_matriz,
    indice_para_letra,
    ler_inteiro_positivo,
    limpar_console,
)

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



    # Definição dos critérios de parada
    print("\n8 - DEFINIÇÃO DOS CRITÉRIOS DE PARADA")
    print("Escolha os critérios de parada para o algoritmo genético:")
    print("1 - Número máximo de gerações")
    print("2 - Convergência (gerações sem melhoria)")
    print("3 - Ambos (o que ocorrer primeiro)")
    entrada = None
    criterio_parada: int = 0
    while entrada is None:
        print("Critério de parada: ", end="", flush=True)
        entrada = ler_inteiro_positivo(1, 3)
        if entrada is not None:
            criterio_parada = entrada
    
    max_geracoes: int = 0
    max_geracoes_sem_melhoria: int = 0
    
    if criterio_parada in [1, 3]:
        entrada = None
        while entrada is None:
            print(f"Digite o número máximo de gerações ({MIN_MAX_GERACOES}-{MAX_MAX_GERACOES}): ", end="", flush=True)
            entrada = ler_inteiro_positivo(MIN_MAX_GERACOES, MAX_MAX_GERACOES)
            if entrada is not None:
                max_geracoes = entrada
                print(f"Número máximo de gerações definido para {max_geracoes}.")
    
    if criterio_parada in [2, 3]:
        entrada = None
        while entrada is None:
            print(f"Digite o número máximo de gerações sem melhoria ({MIN_GERACOES_SEM_MELHORIA}-{MAX_GERACOES_SEM_MELHORIA}): ", end="", flush=True)
            entrada = ler_inteiro_positivo(MIN_GERACOES_SEM_MELHORIA, MAX_GERACOES_SEM_MELHORIA)
            if entrada is not None:
                max_geracoes_sem_melhoria = entrada
                print(f"Número máximo de gerações sem melhoria definido para {max_geracoes_sem_melhoria}.")



    # Inicializando a solução do problema do caixeiro viajante usando algoritmo genético
    input("\nPressione ENTER para iniciar a solução do problema do caixeiro viajante usando algoritmo genético...\n")
    tempo_inicio = time.time()
    pygame.init()
    pygame.display.set_caption("PÓS TECH FIAP - Turma 7IADT/Módulo 02 - TSP Solver")
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    clock = pygame.time.Clock()

    limites_estimados = calcular_limites_estimados(matrizDistancias)
    geracao = 0
    melhores_solucoes: List[Tuple[List[str], float, List[int]]] = []
    melhor_fitness: float = float('inf')
    geracoes_sem_melhoria: int = 0
    criterio_atingido: str = ""

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
        
        # Verificar critérios de convergência
        fitness_atual = populacao_fitness_trajeto[0][1]
        if fitness_atual < melhor_fitness:
            melhor_fitness = fitness_atual
            geracoes_sem_melhoria = 0
        else:
            geracoes_sem_melhoria += 1
        
        # Verificar critérios de parada
        parar_execucao = False
        if criterio_parada == 1 and geracao >= max_geracoes:
            parar_execucao = True
            criterio_atingido = f"Número máximo de gerações atingido ({max_geracoes})"
        elif criterio_parada == 2 and geracoes_sem_melhoria >= max_geracoes_sem_melhoria:
            parar_execucao = True
            criterio_atingido = f"Convergência atingida ({max_geracoes_sem_melhoria} gerações sem melhoria)"
        elif criterio_parada == 3:
            if geracao >= max_geracoes:
                parar_execucao = True
                criterio_atingido = f"Número máximo de gerações atingido ({max_geracoes})"
            elif geracoes_sem_melhoria >= max_geracoes_sem_melhoria:
                parar_execucao = True
                criterio_atingido = f"Convergência atingida ({max_geracoes_sem_melhoria} gerações sem melhoria)"
        
        if parar_execucao:
            emExecucao = False

        tela.fill(COR_BRANCO)
        draw_plot(tela, list(range(len(melhores_solucoes))), [solucao[1] for solucao in melhores_solucoes], y_label="Gráfico de fitness")
        draw_cities(tela, list(cidades.values()), list(cidades.keys()))
        draw_paths(tela, melhores_solucoes[-1], cidades)
        pygame.display.flip()
        clock.tick(FPS)

        print(f"Geração {geracao}: Fitness {melhores_solucoes[-1][1]:5.3f} (Sem melhoria: {geracoes_sem_melhoria}) - Trajeto {melhores_solucoes[-1][0]}, Transportes {melhores_solucoes[-1][2]}\r", end="", flush=True)
        
        # ------------------------------------------------------------
        # Implementação do algoritmo genético: seleção
        # - Utiliza elitismo para iniciar a nova população com os 10% melhores resultados
        # ------------------------------------------------------------
        nova_populacao: List[List[str]] = list(populacao_fitness_trajeto[i][0] for i in range(tamPopulacao // 10))

        # ------------------------------------------------------------
        # Implementação do algoritmo genético: cruzamento
        # - Utiliza toneiro para selecionar os pais;
        # - Utiliza Edge Recombination Crossover (ERX) para gerar os filhos;
        # ------------------------------------------------------------
        while len(nova_populacao) < tamPopulacao:
            p1 = selecao_por_torneio(populacao_fitness_trajeto)
            p2 = selecao_por_torneio(populacao_fitness_trajeto)
            if p1 is not None and p2 is not None:
                nova_populacao.extend(edge_recombination_crossover(p1, p2))
        
        # ------------------------------------------------------------
        # Implementação do algoritmo genético: mutação
        # - Percorre a nova população aplicando mutação na metade inferior dos indivíduos
        # ------------------------------------------------------------
        for i in range(len(nova_populacao) // 2, len(nova_populacao)):
            nova_populacao[i] = aplicar_mutacoes(nova_populacao[i])

        # Finalizando esta geração, definindo a população para a próxima geração
        populacao = nova_populacao[:tamPopulacao]        

    # Finalização
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    
    print(f"\n\n{'='*80}")
    print(f"EXECUÇÃO FINALIZADA")
    print(f"{'='*80}")
    if criterio_atingido:
        print(f"Critério de parada: {criterio_atingido}")
    print(f"Total de gerações: {geracao}")
    print(f"Melhor fitness encontrado: {melhor_fitness:.3f}")
    print(f"Melhor trajeto: {melhores_solucoes[-1][0]}")
    print(f"Transportes utilizados: {melhores_solucoes[-1][2]}")
    print(f"Tempo de execução: {tempo_execucao:.2f}s")
    print(f"{'='*80}")
    
    # Gerar relatório em PDF
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_pdf = gerar_relatorio_pdf(
            num_cidades=numCidades,
            cidades=cidades,
            tamanho_populacao=tamPopulacao,
            total_geracoes=geracao,
            criterio_parada=criterio_atingido if criterio_atingido else "Manual",
            melhor_fitness=melhor_fitness,
            melhor_trajeto=melhores_solucoes[-1][0],
            transportes=melhores_solucoes[-1][2],
            tempo_execucao=tempo_execucao,
            diretorio_saida=diretorio_atual
        )
        print(f"\n✓ Relatório PDF gerado e aberto: {os.path.basename(caminho_pdf)}")
    except Exception as e:
        print(f"\n Erro ao gerar relatório PDF: {e}")
        print("Verifique se o arquivo .env está configurado com sua chave da OpenAI.")
    
    print(f"\nFim do módulo \"{__name__}\"\n")
