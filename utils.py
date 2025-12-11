"""
Biblioteca de funções utilitárias do projeto
"""
import os
import platform
import re



def imprimir_matriz(matriz, largura: int = 8, casasDecimais: int = 1):
    """
    Imprime uma matriz (lista de listas) formatada no console.
    - matriz: lista de listas (n x n)
    - largura: largura fixa de cada coluna (inclui sinal/decimal)
    - casasDecimais: casas decimais para números flutuantes
    """
    if not matriz:
        print("Matriz vazia")
        return

    n = len(matriz)
    fmt = f"{{:>{largura}.{casasDecimais}f}}"

    # cabeçalho de índices
    header = " " * (largura + 1) + " ".join(f"{j:>{largura}d}" for j in range(n))
    print(header)
    print(" " * (largura + 1) + "-" * (n * (largura + 1) - 1))

    for i, row in enumerate(matriz):
        row_str = " ".join(fmt.format(float(val)) for val in row)
        print(f"{i:>{largura}d} {row_str}")



def ler_inteiro_positivo(max: int) -> int:
    
    """
    Lê do stdin até o usuário digitar um número inteiro positivo até o valor especificado.
    Retorna o inteiro validado.
    """

    # regex: números sem sinal, sem casas decimais
    padrao = r'^[1-9]\d*$';

    numero = input().strip()
    if re.match(padrao, numero):
        try:
            value = int(numero)
            if value > 0 and value <= max:
                return value
        except ValueError:
            pass
    print("Entrada inválida!")
    return



def limpar_console():

    """
    Limpa o console em função do sistema operacional
    """
        
    if platform.system().lower().startswith("win"):
        os.system("cls")
    else:
        os.system("clear")
