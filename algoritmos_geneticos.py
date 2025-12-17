from parametros import LIM_CARRO_ELETRICO
from parametros import TIPO_TRANSPORTE_AVIAO, TIPO_TRANSPORTE_TREM, TIPO_TRANSPORTE_CARRO_ELETRICO, TIPO_TRANSPORTE_CAMINHAO
from parametros import VELOC_AVIAO, VELOC_TREM, VELOC_CARRO_ELETRICO, VELOC_CAMINHAO
from parametros import CUSTO_AVIAO, CUSTO_TREM, CUSTO_CARRO_ELETRICO, CUSTO_CAMINHAO
from typing import List, Tuple
import random



def populacao_inicial_aleatoria(cidades: List[str], tamanho_populacao: int) -> List[List[str]]:
    """
    Gera uma população inicial aleatória de rotas para um conjunto dado de cidades e tamanho de população.
    """
    return [random.sample(cidades, len(cidades)) for _ in range(tamanho_populacao)]



def calcular_fitness(
    matrizDistancias: List[List[float]],
    matrizAviao: List[List[int]],
    matrizTrem: List[List[int]],
    individuo: List[str]) -> Tuple[int, List[int]]:
    """
    Calcula o fitness de cada indivíduo na população, preferindo primeiro os veículos mais rápidos:
    1 - Mede o tempo total (buscando o menor tempo);
    2 - Mede o custo total;
    3 - Calcula a relação entre eles;
    4 - Retorna a relação custo/tempo e a rota de transportes utilizados;
    """
    tempo_total:int = 0
    custo_total:int = 0
    lista_transportes: List[int] = []
    for i in range(len(individuo)):

        cidade_atual = individuo[i]
        cidade_proxima = individuo[(i + 1) % len(individuo)]
        indice_atual = ord(cidade_atual) - ord('A')
        indice_proxima = ord(cidade_proxima) - ord('A')
        distancia = int(matrizDistancias[indice_atual][indice_proxima])

        if matrizAviao[indice_atual][indice_proxima] == 1:
            tempo_total += distancia // VELOC_AVIAO
            custo_total += distancia * CUSTO_AVIAO
            lista_transportes.append(TIPO_TRANSPORTE_AVIAO)
        elif matrizTrem[indice_atual][indice_proxima] == 1:
            tempo_total += distancia // VELOC_TREM
            custo_total += distancia * CUSTO_TREM
            lista_transportes.append(TIPO_TRANSPORTE_TREM)
        elif distancia <= LIM_CARRO_ELETRICO:
            tempo_total += distancia // VELOC_CARRO_ELETRICO
            custo_total += distancia * CUSTO_CARRO_ELETRICO
            lista_transportes.append(TIPO_TRANSPORTE_CARRO_ELETRICO)
        else:
            tempo_total += distancia // VELOC_CAMINHAO
            custo_total += distancia * CUSTO_CAMINHAO
            lista_transportes.append(TIPO_TRANSPORTE_CAMINHAO)
    
    return custo_total // tempo_total, lista_transportes