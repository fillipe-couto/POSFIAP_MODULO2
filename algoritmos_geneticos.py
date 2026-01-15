import random
from typing import List, Tuple

from parametros import (
    CUSTO_AVIAO,
    CUSTO_CAMINHAO,
    CUSTO_CARRO_ELETRICO,
    CUSTO_TREM,
    LIM_CARRO_ELETRICO,
    PESO_TEMPO,
    PROB_MUTACAO,
    TIPO_TRANSPORTE_AVIAO,
    TIPO_TRANSPORTE_CAMINHAO,
    TIPO_TRANSPORTE_CARRO_ELETRICO,
    TIPO_TRANSPORTE_TREM,
    VELOC_AVIAO,
    VELOC_CAMINHAO,
    VELOC_CARRO_ELETRICO,
    VELOC_TREM,
)


def populacao_inicial_aleatoria(cidades: List[str], tamanho_populacao: int) -> List[List[str]]:
    """
    Gera uma população inicial aleatória de rotas para um conjunto dado de cidades e tamanho de população.
    """
    return [random.sample(cidades, len(cidades)) for _ in range(tamanho_populacao)]



def calcular_limites_estimados(matriz_distancias: List[List[float]]) -> Tuple[int, int, int, int]:
    """
    Calcula os limites teóricos de tempo e custo para normalização.    
    Retorna uma tupla com [tempo_min, tempo_max, custo_min, custo_max], onde:
    1 - tempo_min: considerando todos os trechos feitos de avião;
    2 - tempo_max: considerando todos os trechos feitos de caminhão;
    3 - custo_min: considerando todos os trechos feitos de carro elétrico;
    4 - custo_max: considerando todos os trechos feitos de avião;
    """
    num_cidades = len(matriz_distancias)
    distancia_total_entre_cidades = sum(sum(linha) for linha in matriz_distancias) / 2    
    dist_media_entre_cidades = distancia_total_entre_cidades / (num_cidades * (num_cidades - 1) / 2)
    dist_media_rota = dist_media_entre_cidades * num_cidades
    
    tempo_min = int(dist_media_rota // VELOC_AVIAO)
    tempo_max = int(dist_media_rota // VELOC_CAMINHAO)    
    custo_min = int(dist_media_rota * CUSTO_CARRO_ELETRICO)
    custo_max = int(dist_media_rota * CUSTO_AVIAO)    
    return tempo_min, tempo_max, custo_min, custo_max



def calcular_fitness_prioridade_tempo(
    matriz_distancias: List[List[float]],
    matriz_aviao: List[List[int]],
    matriz_trem: List[List[int]],
    individuo: List[str],
    tempo_min,
    tempo_max,
    custo_min,
    custo_max,
    peso_tempo: float = PESO_TEMPO) -> Tuple[List[str], float, List[int]]:
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
        distancia = int(matriz_distancias[indice_atual][indice_proxima])

        if matriz_aviao[indice_atual][indice_proxima] == 1:
            tempo_total += distancia // VELOC_AVIAO
            custo_total += distancia * CUSTO_AVIAO
            lista_transportes.append(TIPO_TRANSPORTE_AVIAO)
        elif matriz_trem[indice_atual][indice_proxima] == 1:
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
    return individuo, tempo_norm * peso_tempo + custo_norm * (1 - peso_tempo), lista_transportes



def selecao_por_torneio(
    candidatos: List[Tuple[List[str], float, List[int]]],
    k: int = 3) -> List[str] | None:
    """
    Realiza a seleção por torneio para escolher indivíduos da população a ser cruzada.
    - candidatos: lista possíveis de indivíduos (rotas)"
    - k: pressão seletiva (número de aspirantes por torneio)
    """
    if len(candidatos) == 0:
        return None

    competidores = random.sample(candidatos, k)
    return min(competidores, key = lambda competidor: competidor[1])[0]



def edge_recombination_crossover(p1: List[str], p2: List[str]) -> Tuple[List[str], List[str]]:
    """
    Implementa o cruzamento por recombinação de arestas (Edge Recombination Crossover - ERX) entre dois pais (p1 e p2).
    Este algoritmo preserva as adjacências dos nós (cidades) dos pais ao gerar os filhos, resultando em um melhor desempenho
    para problemas de roteamento, como o Problema do Caixeiro Viajante (TSP).
    Retorna dois filhos resultantes do cruzamento
    """
    # Função auxiliar para construir a tabela de adjacências
    def definir_adjacencias(pai: List[str]) -> dict:
        adj = {}
        n = len(pai)
        for i, v in enumerate(pai):
            if v not in adj: adj[v] = set()
            left = pai[(i-1) % n]
            right = pai[(i+1) % n]
            adj[v].add(left)
            adj[v].add(right)
        return adj

    # Função principal do algoritmo
    def erx(p1, p2):
        
        # Combina as adjacências de ambos os pais
        adj = {}
        for p in (p1, p2):
            for k, v in definir_adjacencias(p).items():
                adj.setdefault(k, set()).update(v)

        # Inicia a construção do filho a partir de um dos nós aleatoriamente
        atual = random.choice(p1)
        filho = []
        while len(filho) < len(p1):            
            
            # Remove o nó atual de todas as listas de adjacência
            filho.append(atual)
            for s in adj.values():
                s.discard(atual)

            # Escolhendo o próximo nó com base na menor lista de adjacência
            if adj[atual]:
                candidatos = list(adj[atual])
                melhor = []
                len_melhor = None
                for c in candidatos:
                    l = len(adj.get(c, ()))
                    if len_melhor is None or l < len_melhor:
                        melhor = [c]
                        len_melhor = l
                    elif l == len_melhor:
                        melhor.append(c)
                atual = random.choice(melhor)
            else:
                # Seleção aleatória entre os nós restantes
                remaining = [x for x in p1 if x not in filho]
                if not remaining:
                    break
                atual = random.choice(remaining)
        return filho

    # Chamada principal da função ERX para gerar dois filhos
    return erx(p1, p2), erx(p2, p1)



def mutacao_swap(individuo: List[str]) -> List[str]:
    """
    Mutação por troca (Swap Mutation): troca dois genes (cidades) de posição aleatoriamente.
    """    
    mutante = individuo.copy()
    n = len(mutante)
    i, j = random.sample(range(n), 2)
    mutante[i], mutante[j] = mutante[j], mutante[i]
    return mutante



def mutacao_inversao(individuo: List[str]) -> List[str]:
    """
    Mutação por inversão (Inversion Mutation): inverte a ordem de um segmento da rota.
    Esta mutação é eficaz para o TSP pois preserva a maioria das adjacências.
    """    
    mutante = individuo.copy()
    n = len(mutante)
    i, j = sorted(random.sample(range(n), 2))
    mutante[i:j+1] = mutante[i:j+1][::-1]
    return mutante



def mutacao_2opt(individuo: List[str]) -> List[str]:
    """
    Mutação 2-opt: remove duas arestas e reconecta a rota de forma diferente.
    Esta mutação é eficaz para o TSP pois preserva a maioria das adjacências.
    """    
    mutante = individuo.copy()
    n = len(mutante)
    i = random.randint(0, n - 2)
    j = random.randint(i + 1, n - 1)
    mutante[i:j+1] = mutante[i:j+1][::-1]
    return mutante



def aplicar_mutacoes(individuo: List[str]) -> List[str]:
    """
    Aplica um operador de mutação aleatoriamente selecionado
    """
    if random.random() > PROB_MUTACAO:
        return individuo
    
    match random.randint(1, 3):
        case 1:
            return mutacao_swap(individuo)
        case 2:
            return mutacao_inversao(individuo)
        case 3:
            return mutacao_2opt(individuo)
        case _:
            return individuo    
