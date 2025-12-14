"""
Biblioteca de funções utilitárias do projeto
"""
import os
import platform
import re



def imprimir_matriz(matriz, largura: int = 8, casasDecimais: int = 0):
    """
    Imprime uma matriz (lista de listas) formatada no console.
    - matriz: lista de listas (n x n)
    - largura: largura fixa de cada coluna (inclui sinal/decimal)
    - casasDecimais: casas decimais para números flutuantes
    """
    if not matriz:
        print("Matriz vazia")
        return

    # função auxiliar: converte índice (0 -> A, 25 -> Z, 26 -> AA, etc.)
    def indice_para_letra(indice: int) -> str:
        letras = []
        i = indice
        while True:
            i, resto = divmod(i, 26)
            letras.append(chr(ord('A') + resto))
            if i == 0:
                return ''.join(reversed(letras))
            i -= 1

    n = len(matriz)
    fmt = f"{{:>{largura}.{casasDecimais}f}}"

    # Impressão do cabeçalho
    labels = [indice_para_letra(j) for j in range(n)]
    header = " " * (largura + 1) + " ".join(f"{label:>{largura}}" for label in labels)
    print(header)
    print(" " * (largura + 1) + "-" * (n * (largura + 1) - 1))

    # Impressão das linhas da matriz
    for i, row in enumerate(matriz):
        row_str = " ".join(fmt.format(float(val)) for val in row)
        row_label = indice_para_letra(i)
        print(f"{row_label:>{largura}} {row_str}")
    print()



def ler_inteiro_positivo(min: int = 0, max: int = 100) -> int | None:
    
    """
    Lê do stdin até o usuário digitar um número inteiro positivo entre os valores especificados.
    Retorna o inteiro validado.
    """

    # regex: números sem sinal, sem casas decimais
    padrao = r'^[1-9]\d*$';

    numero = input().strip()
    if re.match(padrao, numero):
        try:
            value = int(numero)
            if value >= min and value <= max:
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
