import random
from typing import List, Tuple

def populacao_inicial_aleatoria(cidades: List[str], tamanho_populacao: int) -> List[List[str]]:
    """
    Gera uma população inicial aleatória de rotas para um conjunto dado de cidades e tamanho de população.
    """
    return [random.sample(cidades, len(cidades)) for _ in range(tamanho_populacao)]