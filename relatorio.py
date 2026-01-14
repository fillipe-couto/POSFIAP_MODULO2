"""
Módulo para geração de relatório PDF do TSP usando LLM
"""
import json
import os
import platform
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openai import OpenAI
from weasyprint import HTML

# Carrega variáveis do .env
load_dotenv()

MAX_OUTPUT_TOKENS = 2048

def formatar_dados_tsp(
    num_cidades: int,
    cidades: Dict[str, Tuple[int, int]],
    tamanho_populacao: int,
    total_geracoes: int,
    criterio_parada: str,
    melhor_fitness: float,
    melhor_trajeto: List[str],
    transportes: List[int],
    tempo_execucao: float
) -> Dict:
    """Formata os dados do TSP para envio à LLM"""
    
    # Mapear tipos de transporte
    tipo_transporte_map = {
        1: "Avião",
        2: "Trem",
        3: "Carro Elétrico",
        4: "Caminhão"
    }
    
    transportes_formatados = [tipo_transporte_map.get(t, f"Desconhecido({t})") for t in transportes]
    
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
            "num_trechos": len(melhor_trajeto) - 1
        },
        "cidades": {nome: {"x": pos[0], "y": pos[1]} for nome, pos in cidades.items()}
    }


def gerar_relatorio_llm(dados_tsp: Dict) -> Dict:
    """Chama a LLM para gerar o relatório analítico"""
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    system_instructions = """
Você é um analista especializado em otimização e algoritmos genéticos.
O seu público alvo são estudantes e profissionais de tecnologia.
Seja técnico mas didático.
Explique os resultados de forma clara e objetiva.
Gere texto em PT-BR.
Gere JSONs válidos no output.
"""

    user_prompt = f"""
Vou te passar um JSON com dados de uma execução de algoritmo genético para o Problema do Caixeiro Viajante (TSP).

Gere um relatório executivo com:

1) Resumo executivo (3-4 linhas sobre o problema resolvido e resultado obtido)
2) Configuração do algoritmo (bullets com parâmetros principais)
3) Análise do resultado (bullets explicando a qualidade da solução, convergência, etc)
4) Detalhes da solução (rota, transportes, métricas)
5) Conclusões e recomendações (2-3 insights técnicos)

Retorne em JSON no formato:

{{
  "titulo": "Relatório de Otimização - TSP",
  "resumo_executivo": "...",
  "configuracao": ["...", "..."],
  "analise_resultado": ["...", "..."],
  "detalhes_solucao": ["...", "..."],
  "conclusoes": ["...", "..."]
}}

Dados da execução:
{json.dumps(dados_tsp, ensure_ascii=False, indent=2)}
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=MAX_OUTPUT_TOKENS,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        output_text = resp.choices[0].message.content
        relatorio = json.loads(output_text)
        return relatorio
        
    except Exception as e:
        print(f"Erro ao gerar relatório com LLM: {e}")
        # Retorna um relatório básico em caso de erro
        return {
            "titulo": "Relatório de Otimização - TSP",
            "resumo_executivo": f"Problema resolvido com {dados_tsp['configuracao']['num_cidades']} cidades em {dados_tsp['configuracao']['total_geracoes']} gerações.",
            "configuracao": [
                f"População: {dados_tsp['configuracao']['tamanho_populacao']} indivíduos",
                f"Gerações: {dados_tsp['configuracao']['total_geracoes']}",
                f"Critério de parada: {dados_tsp['configuracao']['criterio_parada']}"
            ],
            "analise_resultado": [
                f"Fitness final: {dados_tsp['resultado']['melhor_fitness']}",
                f"Trajeto encontrado: {dados_tsp['resultado']['trajeto']}"
            ],
            "detalhes_solucao": [
                f"Número de trechos: {dados_tsp['resultado']['num_trechos']}",
                f"Transportes: {', '.join(dados_tsp['resultado']['transportes_utilizados'])}"
            ],
            "conclusoes": [
                "Relatório gerado automaticamente (LLM indisponível)"
            ]
        }


def gerar_html_relatorio(relatorio: Dict, dados_tsp: Dict) -> str:
    """Gera o HTML do relatório a partir dos dados usando Jinja2"""
    
    # Configura o ambiente Jinja2
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
    
    # Prepara os dados para o template
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    config = dados_tsp['configuracao']
    resultado = dados_tsp['resultado']
    
    # Renderiza o template com os dados
    html = template.render(
        titulo=relatorio.get('titulo', 'Relatório TSP'),
        data_hora=data_hora,
        resumo_executivo=relatorio.get('resumo_executivo', ''),
        configuracao=relatorio.get('configuracao', []),
        analise_resultado=relatorio.get('analise_resultado', []),
        detalhes_solucao=relatorio.get('detalhes_solucao', []),
        conclusoes=relatorio.get('conclusoes', []),
        num_cidades=config['num_cidades'],
        total_geracoes=config['total_geracoes'],
        melhor_fitness=resultado['melhor_fitness'],
        tempo_execucao=config['tempo_execucao_segundos'],
        trajeto=resultado['trajeto'],
        transportes=', '.join(resultado['transportes_utilizados']),
        criterio_parada=config['criterio_parada']
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
    diretorio_saida: str = "."
) -> str:
    """
    Função principal que gera o relatório completo em PDF
    
    Returns:
        Caminho do arquivo PDF gerado
    """
    
    print("\n" + "="*80)
    print("GERANDO RELATÓRIO EM PDF")
    print("="*80)
    
    # 1. Formatar dados
    print("1/4 - Formatando dados...")
    dados_tsp = formatar_dados_tsp(
        num_cidades, cidades, tamanho_populacao, total_geracoes,
        criterio_parada, melhor_fitness, melhor_trajeto, transportes, tempo_execucao
    )
    
    # 2. Gerar relatório com LLM
    print("2/4 - Gerando análise com LLM...")
    relatorio = gerar_relatorio_llm(dados_tsp)
    
    # 3. Gerar HTML
    print("3/4 - Gerando HTML...")
    html_content = gerar_html_relatorio(relatorio, dados_tsp)
    
    # 4. Converter para PDF
    print("4/4 - Convertendo para PDF...")
    nome_arquivo = "relatorio_tsp.pdf"
    caminho_pdf = os.path.join(diretorio_saida, nome_arquivo)
    
    HTML(string=html_content).write_pdf(caminho_pdf)
    
    print(f"✓ Relatório gerado com sucesso: {caminho_pdf}")
    print("="*80 + "\n")
    
    # 5. Abrir PDF automaticamente
    abrir_pdf(caminho_pdf)
    
    return caminho_pdf
