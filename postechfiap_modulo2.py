from utils import imprimir_matriz, ler_inteiro_positivo, limpar_console
import random
import math



# Constantes/macros
MAX_CIDADES = 12
LARGURA_TERRENO = 1200
ALTURA_TERRENO = 800


# Exemplo de uso
if __name__ == "__main__":

    # Introdução
    limpar_console()
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("*                  POS-TECH FIAP - Módulo 02                  *")
    print("*                  IA PARA DEV - TURMA 7IADT                  *")
    print("*   PROJETO 2 - Solução para o problema do Caixeiro Viajante  *")
    print("*            (TSP - Traveling Salesperson Problem)            *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n\n")
    
    # Definição do número de cidades
    print("1 - DEFINIÇÃO DO NÚMERO DE CIDADES")
    entradaValida = False
    numCidades = None
    posCidades = None
    matrizDistancias = None
    while not entradaValida:
        print(f"    Digite um número inteiro positivo maior que 5 e menor ou igual a {MAX_CIDADES}: ", end="", flush=True)
        numCidades = ler_inteiro_positivo(MAX_CIDADES)
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
        for j in range(i+1, numCidades):
            xj, yj = posCidades[j]
            d = math.hypot(xi - xj, yi - yj)
            matrizDistancias[i][j] = d
            matrizDistancias[j][i] = d
    print(f"Matriz de distâncias calculada: \n")
    imprimir_matriz(matrizDistancias)

    # Finalização
    print("\n* * * Fim do programa * * *\n")
