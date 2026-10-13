# **Regras de Contexto e Governança de IA (CONTEXT_RULES)**

**Documento:** Regras de Contexto e Governança de IA  
**Versão:** 3.1.0 (Atualizado para Módulo Nativo `src/task_analyzer`, Portabilidade e Validação via Pytest)  

---

## **1. Identificação do Documento e Aluno**

| Campo | Informação |
| :--- | :--- |
| **Nome do Aluno** | João Pedro de Melo Naves |
| **Matrícula** | 22509476 |
| **Curso** | Análise e Desenvolvimento de Sistemas |
| **Polo / Turma** | Asa Norte – Turma A |
| **E-mail Institucional** | joao.naves@sempreceub.com |
| **Arquivo de Destino no Repositório** | `CONTEXT_RULES.md` |

---

## **2. Objetivos e Finalidade das Regras Persistentes**

Este documento estabelece a **Versão 3.1.0 das Regras de Contexto e Governança de IA** atreladas ao repositório do projeto **TaskAnalyzer**. Ele serve como instrução permanente (*system prompt / context instructions*) para agentes e modelos de inteligência artificial encarregados de gerar, refatorar, testar e revisar o código do projeto, garantindo conformidade com o ecossistema **Anaconda/Conda**, portabilidade entre ambientes de execução e execução automatizada via **Pytest**.

---

## **3. Diretrizes Arquiteturais Obrigatórias**

- **Versão Mínima do Python:** O código gerado deve ser estritamente compatível com **Python 3.11+**.
- **Ecossistema Anaconda.org:** O ambiente de desenvolvimento e avaliação deve utilizar o gerenciador **Conda** (definido no arquivo `environment.yml` com o ambiente denominado `task-analyzer`) para reprodutibilidade total das dependências.
- **Estrutura de Pacote Padrão:** O código-fonte da aplicação deve residir no pacote Python `src/task_analyzer/`, evitando nomenclaturas específicas de frameworks web (como `blueprints`).
- **Anotação de Tipos (Type Hints):** Obrigatoriedade do uso de anotações de tipos em 100% dos métodos, funções, parâmetros e retornos públicos e privados.
- **Princípios de Código Limpo e SRP:** Aderência ao *Single Responsibility Principle* (SRP) e conformidade total com o guia de estilo **PEP 8**.
- **Documentação Formal (Google Style Docstrings):** Módulos, classes, funções e parâmetros devem ser documentados no formato Google Docstring.
- **Tratamento de Exceções:** Lançamento e captura explícita de exceções específicas com mensagens claras e contextuais.
- **Logging Estruturado Nativo:** Utilização exclusiva do módulo padrão `logging` do Python configurado para saídas organizadas em `stdout`/`stderr`.
- **Portabilidade de Ambiente:** Proibição de inclusão de arquivos de configuração específicos de IDE (`.vscode/`, `.idea/`) no repositório de versão. A reprodutibilidade do ambiente deve ser garantida via `environment.yml` e `.gitignore`.

---

## **4. Sessão de Proibições Explícitas (Regras Restritivas)**

Fica terminantemente proibido para a Inteligência Artificial e para o desenvolvedor durante a geração e manutenção do código:

1. **Uso de Bibliotecas Externas Não Autorizadas em Runtime:** Permitido apenas o uso das bibliotecas homologadas no ambiente `task-analyzer` do Conda e a Biblioteca Padrão (*Standard Library*) do Python em tempo de execução. O uso de `pytest` é restrito à suíte de testes e automação CI/CD.
2. **Alteração de Cenários de Teste Fornecidos:** Proibido modificar, desativar, ignorar ou adaptar a suíte de testes em `tests/test_harness.py` sem autorização prévia.
3. **Alteração da Estrutura Padrão de Diretórios:** A árvore do repositório deve seguir rigorosamente a estrutura definida na Seção 5.
4. **Persistência de Dados em Disco ou Banco de Dados:** O processamento é 100% em memória (*In-Memory*). Proibida a gravação de arquivos temporários (JSON, CSV, SQLite) em disco ou conexões externas.
5. **Alteração da Assinatura de Funções Públicas:** Proibido renomear métodos públicos ou alterar a ordem e tipo dos parâmetros expostos no contrato analítico.
6. **Comitação de Configurações Locais de Editor:** Proibida a inclusão da pasta `.vscode/` ou atalhos locais de sistema no controle de versão Git.
7. **Geração de Código sem Cobertura de Testes:** Nenhuma nova função analítica deve ser entregue sem os respectivos testes unitários em `pytest`.

---

## **5. Estrutura Padrão do Repositório GitHub (Árvore de Projetos)**

```text
BootCampIII-TaskAnalyzer/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline CI/CD (GitHub Actions com setup-miniconda e Pytest)
├── .gitignore                 # Exclusão de .vscode/, __pycache__, .pytest_cache e ambientes locais
├── README.md                  # Instruções de reprodução (Conda + Pytest)
├── CONTEXT_RULES.md           # Regras de governança de IA e contexto (v3.1.0)
├── environment.yml            # Definição de ambiente Conda (Python 3.11 + Pytest)
├── specs/
│   └── task_analyzer_spec.md  # Especificação Técnica SDD (v4.1.0)
├── tests/
│   └── test_harness.py        # Suíte de testes automatizados via Pytest
└── src/
    └── task_analyzer/         # Pacote principal com a lógica analítica em memória
        ├── __init__.py
        ├── core.py            # Execução de métricas e processamento de tarefas
        └── utils.py           # Funções auxiliares de validação e formatação
```