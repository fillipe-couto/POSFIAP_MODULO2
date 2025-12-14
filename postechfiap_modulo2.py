from utils import imprimir_matriz, ler_inteiro_positivo, limpar_console
import random
import math



# Constantes/macros de configuração
MIN_CIDADES = 6
MAX_CIDADES = 18
LARGURA_TERRENO = 400
ALTURA_TERRENO = 300
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
    entradaValida = False
    numCidades = None | int
    posCidades = None
    matrizDistancias = None
    perc_cnx_trem = 0
    qtd_cnx_trem = None
    matrizTrem = None
    while not entradaValida:
        print(f"Digite um número inteiro positivo maior ou igual a {MIN_CIDADES} e menor ou igual a {MAX_CIDADES}: ", end="", flush=True)
        numCidades = ler_inteiro_positivo(MIN_CIDADES, MAX_CIDADES)
        if numCidades is not None:
            entradaValida = True
            print(f"Número de cidades definido para {numCidades}.\n")



    # Definindo posicionamento das cidades aleatoriamente
    print("2 - POSICIONAMENTO ALEATÓRIO DAS CIDADES")
    posCidades = [(random.randint(0, LARGURA_TERRENO), random.randint(0, ALTURA_TERRENO)) for _ in range(numCidades)]
    print(f"Cidades posicionadas aleatoriamente em um terreno de {LARGURA_TERRENO} x {ALTURA_TERRENO}:\n{posCidades}\n")



    # Calculando a distância euclidiana de cada par de cidades para montar a matriz de distâncias
    print("3 - DEFININDO MATRIZ DE DISTÂNCIAS ENTRE AS CIDADES")
    matrizDistancias = [[0.0 for _ in range(numCidades)] for _ in range(numCidades)]
    for i in range(numCidades):
        xi, yi = posCidades[i]
        for j in range(i + 1, numCidades):
            xj, yj = posCidades[j]
            d = math.hypot(xi - xj, yi - yj)
            matrizDistancias[i][j] = d
            matrizDistancias[j][i] = d
    print("Matriz de distâncias calculada: \n")
    imprimir_matriz(matrizDistancias)



    # Calculando a distância euclidiana de cada par de cidades para montar a matriz de distâncias
    print("4 - DEFININDO ALEATORIAMENTE ROTAS POSSÍVEIS DE TREM ENTRE AS CIDADES")
    entradaValida = False
    while not entradaValida:
        print(f"Digite um percentual válido entre 0 e 100 para a proporção de rotas possíveis de trem: ", end="", flush=True)
        perc_cnx_trem = ler_inteiro_positivo(0, 100)
        if perc_cnx_trem is not None:
            entradaValida = True
    qtd_cnx_trem = (numCidades * (numCidades - 1) // 2) * perc_cnx_trem // 100
    print(f"Percentual de rotas de trem definido para {perc_cnx_trem}%, resultando em {qtd_cnx_trem} rotas possíveis.\n")
    vetor_rotas_trem = list(range(1, (numCidades * (numCidades - 1) // 2) + 1, 1))
    rotas_trem = sorted(random.sample(vetor_rotas_trem, k = qtd_cnx_trem))
    print(vetor_rotas_trem, rotas_trem)
    matrizTrem = [[0 for _ in range(numCidades)] for _ in range(numCidades)]
    print("Matriz de rotas de trem: \n")
    imprimir_matriz(matrizTrem)



    # Finalização
    print(f"Fim do módulo \"{__name__}\"\n")
