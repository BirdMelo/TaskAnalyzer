# **Software Design Document (SDD) — TaskAnalyzer**

**Documento:** Software Design Document (SDD) — TaskAnalyzer  
**Versão:** 4.1.0 (Atualizado para Python 3.11+, Pacote `src/task_analyzer`, Portabilidade e Processamento In-Memory)  

---

## **1. Identificação do Projeto e Aluno**

| Campo | Informação |
| :--- | :--- |
| **Nome do Aluno** | João Pedro de Melo Naves |
| **Matrícula** | 22509476 |
| **Curso** | Análise e Desenvolvimento de Sistemas |
| **Polo / Turma** | Asa Norte – Turma A |
| **E-mail Institucional** | joao.naves@sempreceub.com |
| **Versão do Documento** | 4.1.0 |

---

## **2. Propósito e Escopo do Módulo TaskAnalyzer**

O **TaskAnalyzer** é um módulo de análise de produtividade desenvolvido em Python 3.11+ e gerenciado através do ecossistema **Anaconda/Conda**. Sua finalidade é processar estruturas de dados de tarefas em memória, calculando métricas de eficiência, retrabalho e adesão a prazos de forma determinística, sem dependência de bancos de dados ou persistência em disco.

### **2.1 Indicadores Processados**

- **Tempo Médio de Conclusão:** Cálculo do tempo decorrido entre o início efetivo ($started\_at$) e o encerramento ($completed\_at$) das tarefas concluídas, expresso em horas decimais.
- **Taxa de Atraso (*Delay Rate*):** Percentual de tarefas concluídas em que a data de encerramento superou a data limite estipulada ($due\_date$).
- **Métricas Segmentadas por Prioridade:** Agrupamento de tempo médio de execução e taxa de atraso pelas categorias de prioridade (`ALTA`, `MEDIA`, `BAIXA`).
- **Taxa de Refação (*Rework Rate*):** Percentual de tarefas que apresentaram reaberturas ou retrabalho ($rework\_count > 0$).

---

## **3. Arquitetura e Decisões Técnicas**

| Componente / Requisito | Especificação Técnica | Justificativa / Diretriz |
| :--- | :--- | :--- |
| **Linguagem de Programação** | Python 3.11+ | Garantia de desempenho otimizado, suporte a Type Hints avançados e estabilidade. |
| **Gerenciamento de Ambiente** | Anaconda/Conda (`environment.yml`) | Isolamento completo de ambiente (`task-analyzer`) garantindo reprodutibilidade em qualquer SO. |
| **Framework de Testes** | `pytest` | Suíte de testes automatizados para validação contínua local e em pipeline de CI/CD. |
| **Estrutura de Código** | Layout `src/task_analyzer/` | Padrão recomendado pela comunidade Python, evitando aclopamento a frameworks web. |
| **Portabilidade de IDE** | `.gitignore` configurado | Supressão da pasta `.vscode/` e arquivos temporários do Git para garantir neutralidade no ambiente do avaliador. |
| **Modelo de Persistência** | Em Memória (*In-Memory*) | Processamento rápido com recebimento de dados via estruturas nativas (`list`, `dict`), sem IO de disco. |

---

## **4. Estrutura do Repositório (Árvore de Arquivos)**

```text
BootCampIII-TaskAnalyzer/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline CI/CD (GitHub Actions com setup-miniconda e Pytest)
├── .gitignore                 # Exclusão de .vscode/, __pycache__, .pytest_cache e ambientes locais
├── README.md                  # Visão geral do projeto e instruções de execução
├── CONTEXT_RULES.md           # Arquivo de regras persistentes para IA (v3.1.0)
├── environment.yml            # Definição do ambiente Conda (Python 3.11 + Pytest)
├── specs/
│   └── task_analyzer_spec.md  # Especificação SDD (v4.1.0)
├── tests/
│   └── test_harness.py        # Suíte de testes automatizados via Pytest
└── src/
    └── task_analyzer/         # Código-fonte principal do pacote
        ├── __init__.py
        ├── core.py            # Implementação das métricas analíticas
        └── utils.py           # Utilitários de validação e cálculo de datas
```

---

## **5. Diretrizes Arquiteturais e Governança de IA**

### **5.1 Boas Práticas e Padrões de Código**

- **Type Hints Integrais:** Tipagem explícita em todos os argumentos, retornos e estruturas internas.
- **Single Responsibility Principle (SRP):** Separação estrita entre parsing/validação de dados (`utils.py`) e consolidação de métricas (`core.py`).
- **Google Style Docstrings:** Documentação padronizada detalhando parâmetros, tipos e exceções disparadas.
- **Logging Estruturado:** Uso do módulo nativo `logging` para rastreabilidade de processamento.

### **5.2 Proibições Explícitas**

1. **Proibido o uso de dependências externas não homologadas:** Permitidos apenas a biblioteca padrão do Python e os pacotes declarados no `environment.yml`.
2. **Proibido alterar cenários de teste:** O arquivo `tests/test_harness.py` é congelado para avaliação.
3. **Proibida a persistência em disco ou DB:** Toda a execução opera exclusivamente em memória RAM.
4. **Proibido alterar a assinatura pública:** Nomes de funções e tipos de parâmetros em `core.py` devem manter estrita retrocompatibilidade.
5. **Proibida a inclusão de configurações locais de IDE:** `.vscode/` deve permanecer no `.gitignore`.

---

## **6. Contrato Executável e Assinaturas em Python (`src/task_analyzer/core.py`)**

```python
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def calculate_productivity_metrics(
    tasks: List[Dict[str, Any]], 
    priority_filter: Optional[str] = "TODAS"
) -> Dict[str, Any]:
    """Calcula métricas de produtividade a partir de uma lista de tarefas em memória.

    Args:
        tasks (List[Dict[str, Any]]): Lista de dicionários contendo os dados das tarefas.
        priority_filter (Optional[str]): Filtro opcional por prioridade ("ALTA", "MEDIA", "BAIXA", "TODAS").

    Returns:
        Dict[str, Any]: Dicionário com estatísticas globais (tempo médio, taxa de atraso,
            taxa de refação e métricas agrupadas).

    Raises:
        ValueError: Se a lista de tarefas contiver incoerência temporal (ex: started_at > completed_at)
            ou formatos inválidos.
    """
    # Lógica analítica em memória executada dentro do ambiente Anaconda 'task-analyzer'
    pass
```