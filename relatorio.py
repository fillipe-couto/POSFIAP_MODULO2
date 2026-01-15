import os
import platform
import subprocess
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from llm import gerar_analise_tsp_llm
from parametros import TIPO_TRANSPORTE_MAP


def calcular_estatisticas_uso_transporte(transportes: List[int]) -> List[Dict]:
    contagem = Counter(transportes)
    
    estatisticas = []
    for tipo_id in sorted(contagem.keys(), key=lambda x: contagem[x], reverse=True):
        estatisticas.append({
            "nome": TIPO_TRANSPORTE_MAP[tipo_id],
            "quantidade": contagem[tipo_id],
            "tipo_id": tipo_id
        })
    
    return estatisticas


def calcular_estatisticas_distancia_transporte(
    transportes: List[int],
    melhor_trajeto: List[str],
    matriz_distancias: List[List[float]],
    estatisticas_uso: List[Dict]
) -> List[Dict]:
    distancias_por_tipo = {tipo_id: 0.0 for tipo_id in TIPO_TRANSPORTE_MAP.keys()}
    
    for i, tipo_transporte in enumerate(transportes):
        cidade_atual = melhor_trajeto[i]
        cidade_proxima = melhor_trajeto[(i + 1) % len(melhor_trajeto)]
        
        idx_atual = ord(cidade_atual) - ord('A')
        idx_proxima = ord(cidade_proxima) - ord('A')
        
        distancia = matriz_distancias[idx_atual][idx_proxima]
        distancias_por_tipo[tipo_transporte] += distancia
    
    estatisticas_com_distancia = []
    for stat in estatisticas_uso:
        nova_stat = stat.copy()
        nova_stat['distancia_km'] = round(distancias_por_tipo[stat['tipo_id']], 1)
        estatisticas_com_distancia.append(nova_stat)
    
    return sorted(
        [s for s in estatisticas_com_distancia if s['distancia_km'] > 0],
        key=lambda x: x['distancia_km'],
        reverse=True
    )


def formatar_dados_tsp(
    num_cidades: int,
    cidades: Dict[str, Tuple[int, int]],
    tamanho_populacao: int,
    total_geracoes: int,
    criterio_parada: str,
    melhor_fitness: float,
    melhor_trajeto: List[str],
    transportes: List[int],
    tempo_execucao: float,
    matriz_distancias: List[List[float]]
) -> Dict:
    transportes_formatados = [TIPO_TRANSPORTE_MAP[t] for t in transportes]
    
    estatisticas_transporte = calcular_estatisticas_uso_transporte(transportes)
    
    estatisticas_distancia = calcular_estatisticas_distancia_transporte(
        transportes,
        melhor_trajeto,
        matriz_distancias,
        estatisticas_transporte
    )
    
    return {
        "configuracao": {
            "num_cidades": num_cidades,
            "tamanho_populacao": tamanho_populacao,
            "total_geracoes": total_geracoes,
            "criterio_parada": criterio_parada,
            "tempo_execucao_segundos": round(tempo_execucao, 2)
        },
        "resultado": {
            "melhor_fitness": round(melhor_fitness, 3),
            "trajeto": " → ".join(melhor_trajeto),
            "transportes_utilizados": transportes_formatados,
            "num_trechos": len(melhor_trajeto) - 1,
            "estatisticas_transporte": estatisticas_transporte,
            "estatisticas_distancia": estatisticas_distancia
        },
        "cidades": {nome: {"x": pos[0], "y": pos[1]} for nome, pos in cidades.items()}
    }


def gerar_html_relatorio(analise_llm: Dict, dados_tsp: Dict) -> str:    
    # Configura o ambiente Jinja2 (Template Processing)
    template_dir = os.path.dirname(__file__)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    try:
        template = env.get_template('template_relatorio.html')
    except Exception as e:
        raise FileNotFoundError(
            f"Template HTML não encontrado: {os.path.join(template_dir, 'template_relatorio.html')}\n"
            f"Certifique-se de que o arquivo 'template_relatorio.html' está no mesmo diretório do relatorio.py\n"
            f"Erro: {e}"
        )
    
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    config = dados_tsp['configuracao']
    resultado = dados_tsp['resultado']
    
    # Renderiza o template com os dados
    html = template.render(
        titulo=analise_llm.get('titulo', 'Análise de Otimização - Traveling Salesman Problem (TSP) - Algoritmo Genético'),
        data_hora=data_hora,
        resumo_executivo=analise_llm.get('resumo_executivo', ''),
        # Dados técnicos (não gerados por LLM)
        num_cidades=config['num_cidades'],
        tamanho_populacao=config['tamanho_populacao'],
        total_geracoes=config['total_geracoes'],
        criterio_parada=config['criterio_parada'],
        tempo_execucao=config['tempo_execucao_segundos'],
        melhor_fitness=resultado['melhor_fitness'],
        num_trechos=resultado['num_trechos'],
        trajeto=resultado['trajeto'],
        transportes=', '.join(resultado['transportes_utilizados']),
        estatisticas_transporte=resultado.get('estatisticas_transporte', []),
        estatisticas_distancia=resultado.get('estatisticas_distancia', []),
        # Análises geradas por LLM
        analise_convergencia=analise_llm.get('analise_convergencia', []),
        analise_solucao=analise_llm.get('analise_solucao', []),
        analise_logistica=analise_llm.get('analise_logistica', []),
        insights_tecnicos=analise_llm.get('insights_tecnicos', []),
        recomendacoes=analise_llm.get('recomendacoes', [])
    )
    
    return html


def abrir_pdf(caminho_pdf: str):
    """Abre o PDF automaticamente no sistema operacional"""
    sistema = platform.system()
    
    try:
        if sistema == "Windows":
            os.startfile(caminho_pdf)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", caminho_pdf], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", caminho_pdf], check=True)
        print(f"PDF aberto automaticamente: {caminho_pdf}")
    except Exception as e:
        print(f"Não foi possível abrir o PDF automaticamente: {e}")
        print(f"Você pode abrir manualmente: {caminho_pdf}")


def gerar_relatorio_pdf(
    num_cidades: int,
    cidades: Dict[str, Tuple[int, int]],
    tamanho_populacao: int,
    total_geracoes: int,
    criterio_parada: str,
    melhor_fitness: float,
    melhor_trajeto: List[str],
    transportes: List[int],
    tempo_execucao: float,
    matriz_distancias: List[List[float]],
    diretorio_saida: str = "."
) -> str:
    print("\n" + "="*80)
    print("GERANDO RELATÓRIO EM PDF")
    print("="*80)
    
    print("1/4 - Formatando dados...")
    dados_tsp = formatar_dados_tsp(
        num_cidades, cidades, tamanho_populacao, total_geracoes,
        criterio_parada, melhor_fitness, melhor_trajeto, transportes, tempo_execucao,
        matriz_distancias
    )
    
    print("2/4 - Gerando análise inteligente com LLM...")
    analise_llm = gerar_analise_tsp_llm(dados_tsp)
    
    print("3/4 - Gerando HTML...")
    html_content = gerar_html_relatorio(analise_llm, dados_tsp)
    
    print("4/4 - Convertendo para PDF...")
    nome_arquivo = "relatorio_tsp.pdf"
    caminho_pdf = os.path.join(diretorio_saida, nome_arquivo)
    
    HTML(string=html_content).write_pdf(caminho_pdf)
    
    print(f"✓ Relatório gerado com sucesso: {caminho_pdf}")
    print("="*80 + "\n")
    
    abrir_pdf(caminho_pdf)
    
    return caminho_pdf
