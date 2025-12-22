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



def calcular_limites_estimados(matrizDistancias: List[List[float]]) -> Tuple[int, int, int, int]:
    """
    Calcula os limites teóricos de tempo e custo para normalização.    
    Retorna uma tupla com [tempo_min, tempo_max, custo_min, custo_max], onde:
    1 - tempo_min: considerando todos os trechos feitos de avião;
    2 - tempo_max: considerando todos os trechos feitos de caminhão;
    3 - custo_min: considerando todos os trechos feitos de carro elétrico;
    4 - custo_max: considerando todos os trechos feitos de avião;
    """
    numCidades = len(matrizDistancias)
    distancia_total_entre_cidades = sum(sum(linha) for linha in matrizDistancias) / 2    
    dist_media_entre_cidades = distancia_total_entre_cidades / (numCidades * (numCidades - 1) / 2)
    dist_media_rota = dist_media_entre_cidades * numCidades
    
    tempo_min = int(dist_media_rota // VELOC_AVIAO)
    tempo_max = int(dist_media_rota // VELOC_CAMINHAO)    
    custo_min = int(dist_media_rota * CUSTO_CARRO_ELETRICO)
    custo_max = int(dist_media_rota * CUSTO_AVIAO)    
    return tempo_min, tempo_max, custo_min, custo_max



def calcular_fitness_prioridade_tempo(
    matrizDistancias: List[List[float]],
    matrizAviao: List[List[int]],
    matrizTrem: List[List[int]],
    individuo: List[str],
    tempo_min,
    tempo_max,
    custo_min,
    custo_max,
    pesoTempo: float = 0.5) -> Tuple[List[str], float, List[int]]:
    """
    Calcula o fitness de cada indivíduo na população, preferindo primeiro os veículos mais rápidos:
    1 - Mede o tempo total (buscando o menor tempo por transportes mais rápidos);
    2 - Mede o custo total;
    3 - Calcula a relação entre eles ponderada pelo peso do tempo;
    4 - Retorna a relação tempo*custo ponderada e a rota de transportes utilizados;
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
    
    tempo_norm = (tempo_total - tempo_min) / (tempo_max - tempo_min)    
    custo_norm = (custo_total - custo_min) / (custo_max - custo_min)    
    return individuo, tempo_norm * pesoTempo + custo_norm * (1 - pesoTempo), lista_transportes
