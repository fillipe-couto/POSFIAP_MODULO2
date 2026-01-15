import json
import os
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI

from parametros import LLM_MAX_OUTPUT_TOKENS, LLM_TEMPERATURE

# Carrega variáveis do .env
load_dotenv()


def gerar_analise_tsp_llm(dados_tsp: Dict) -> Dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # System prompt: define persona, tom e regras gerais (reutilizável)
    system_instructions = """
Você é um especialista sênior em algoritmos genéticos e otimização logística.
Seu papel é analisar resultados de experimentos e fornecer insights técnicos profundos sobre algoritmos e operações de transporte.

Sempre:
- Seja técnico e didático
- Seja sucinto, não repita informações
- Use linguagem clara e objetiva em PT-BR
- Pense como um analista de logística ao avaliar transportes
"""

    # User prompt: tarefa específica, dados, instruções detalhadas e formato de saída
    user_prompt = f"""
Analise esta execução de algoritmo genético aplicado ao TSP (Traveling Salesperson Problem).

DADOS DA EXECUÇÃO:
{json.dumps(dados_tsp, ensure_ascii=False, indent=2)}

INSTRUÇÕES IMPORTANTES:
- NÃO repita dados brutos (trajeto, fitness, gerações) - eles já estão visíveis no relatório
- FOQUE em: interpretação qualitativa, eficiência do algoritmo, insights técnicos e recomendações
- Para análise logística: avalie eficiência modal, custo-benefício, distribuição de carga, e otimização de frota
- Use formato de bullets para facilitar leitura

Gere uma análise estruturada em JSON seguindo exatamente esta estrutura:

{{
  "titulo": "Análise de Otimização - Traveling Salesman Problem (TSP) - Algoritmo Genético",
  "resumo_executivo": "Parágrafo de 3-4 linhas contextualizando o problema, resultado principal e eficiência computacional",
  "analise_convergencia": [
    "Bullet avaliando a convergência do algoritmo",
    "Bullet sobre qualidade da solução encontrada",
    "Bullet sobre eficiência das gerações",
    "Bullet sugerindo possíveis melhorias no processo"
  ],
  "analise_solucao": [
    "Bullet interpretando o valor de fitness obtido",
    "Bullet avaliando distribuição de transportes usados",
    "Bullet comentando viabilidade prática da rota",
    "Bullet comparando com expectativas teóricas"
  ],
  "analise_logistica": [
    "Bullet sobre eficiência modal (qual transporte mais adequado)",
    "Bullet sobre otimização de custo vs tempo baseado nos transportes escolhidos",
    "Bullet sobre distribuição de distâncias por tipo de transporte",
    "Bullet sobre recomendações operacionais e estratégicas"
  ],
  "insights_tecnicos": [
    "Bullet identificando padrões na solução",
    "Bullet destacando características interessantes",
    "Bullet comentando aspectos únicos desta instância"
  ],
  "recomendacoes": [
    "Bullet sugerindo melhorias para execuções futuras",
    "Bullet recomendando ajustes de parâmetros",
    "Bullet com considerações para problemas similares"
  ]
}}

Retorne APENAS o JSON válido, sem markdown ou texto extra.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            temperature=LLM_TEMPERATURE,
            response_format={"type": "json_object"}
        )
        
        output_text = resp.choices[0].message.content
        analise = json.loads(output_text)
        return analise
        
    except Exception as e:
        print(f"⚠ Erro ao gerar análise com LLM: {e}")
        # Retorna análise básica em caso de erro
        return {
            "titulo": "Análise de Otimização - Problema do Caixeiro Viajante",
            "resumo_executivo": f"Algoritmo genético aplicado ao TSP com {dados_tsp['configuracao']['num_cidades']} cidades, convergindo em {dados_tsp['configuracao']['total_geracoes']} gerações.",
            "analise_convergencia": [
                f"O algoritmo convergiu após {dados_tsp['configuracao']['total_geracoes']} gerações.",
                f"População de {dados_tsp['configuracao']['tamanho_populacao']} indivíduos utilizada.",
                "Análise detalhada indisponível (LLM offline)."
            ],
            "analise_solucao": [
                f"Fitness final obtido: {dados_tsp['resultado']['melhor_fitness']}",
                f"Solução encontrada utiliza {dados_tsp['resultado']['num_trechos']} trechos.",
                "Análise qualitativa indisponível (LLM offline)."
            ],
            "analise_logistica": [
                "Análise logística indisponível (LLM offline).",
                "Execute novamente com conexão ativa para análise detalhada de transportes."
            ],
            "insights_tecnicos": [
                "Análise de padrões indisponível (LLM offline)."
            ],
            "recomendacoes": [
                "Execute novamente para obter análise completa com LLM.",
                "Verifique configuração da chave API da OpenAI."
            ]
        }

