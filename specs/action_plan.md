# Plano de Ação — TaskAnalyzer

## Objetivo

Implementar o TaskAnalyzer como um pacote Python 3.11+ para análise
determinística de produtividade, com processamento exclusivamente em memória,
testes automatizados e pipeline de integração contínua.

Todas as etapas serão executadas individualmente. Uma etapa somente será
iniciada após autorização explícita.

## Regras de execução para futuras implementações

- Cada implementação deve ser realizada em uma branch diferente.
- Os nomes das branches devem seguir a convenção do Git, preferencialmente com
  o prefixo `feature/`, `fix/` ou `test/` e descrição em kebab-case.
- Nenhum commit deve ser criado sem autorização explícita.
- As mensagens de commit devem seguir Conventional Commits e ser escritas em
  português do Brasil.
- Toda implementação deve registrar neste plano o que foi alterado,
  implementado e removido.
- Decisões importantes sobre arquitetura, comportamento, contrato público,
  dependências, formato de saída, versionamento ou testes devem ser
  apresentadas ao responsável com alternativas antes da implementação.
- Arquivos que contenham versionamento devem ser atualizados de forma
  consistente, incluindo `pyproject.toml` e `src/task_analyzer/__init__.py`.

## Diretrizes obrigatórias

- Utilizar Conda conforme o ambiente definido em `environment.yml`.
- Manter o código-fonte em `src/task_analyzer/`.
- Manter compatibilidade com Python 3.11 ou superior.
- Usar somente a biblioteca padrão em runtime e as dependências homologadas.
- Aplicar PEP 8, princípios de responsabilidade única e type hints integrais.
- Documentar módulos, classes, funções e parâmetros com Google Style Docstrings.
- Usar o módulo padrão `logging` para registros estruturados.
- Processar todos os dados em memória, sem arquivos temporários, banco de dados
  ou conexões externas.
- Preservar as assinaturas públicas definidas na especificação técnica.
- Não alterar os cenários fornecidos em `tests/test_harness.py` sem autorização.
- Entregar cada nova função analítica com testes unitários correspondentes.

## Etapas de implementação

### 1. Build e estrutura inicial — concluída

- Configurar o pacote Python com layout `src/`.
- Criar `src/task_analyzer/`.
- Configurar `pyproject.toml` para build e descoberta do pacote.
- Configurar a execução do Pytest.
- Criar a documentação inicial no `README.md`.
- Validar instalação editável, compilação e importação do pacote.

### 2. Validações e utilitários — concluída

**Objetivo:** criar a camada responsável pela validação e normalização dos
dados de tarefas.

**Implementações previstas:**

- Validar campos obrigatórios de cada tarefa.
- Validar os formatos de `started_at`, `completed_at` e `due_date`.
- Validar a coerência temporal dos intervalos.
- Validar prioridades permitidas: `ALTA`, `MEDIA` e `BAIXA`.
- Validar `rework_count`.
- Criar funções auxiliares pequenas e com responsabilidade única em `utils.py`.
- Registrar erros relevantes com `logging`.
- Validar sem modificar os dados recebidos.
- Interromper na primeira inconsistência com `ValueError` contextualizado.

**Testes previstos:**

- Casos válidos.
- Campos ausentes.
- Tipos inválidos.
- Datas em formato inválido.
- Intervalos temporais incoerentes.
- Prioridades inválidas.
- Valores inválidos de retrabalho.

**Implementação realizada:**

- Criadas `parse_datetime`, `validate_task` e `validate_tasks` em
  `src/task_analyzer/utils.py`.
- Adicionada validação de campos obrigatórios, datas ISO 8601, coerência
  temporal, prioridades e contagem de retrabalho.
- Adicionados testes unitários em `tests/test_utils.py`.
- Atualizada a documentação do projeto para refletir a conclusão da etapa.

### 3. Métricas analíticas — concluída

**Objetivo:** implementar o contrato
`calculate_productivity_metrics` em `core.py`.

**Métricas previstas:**

- Tempo médio de conclusão em horas decimais.
- Taxa de atraso.
- Métricas agrupadas por prioridade.
- Taxa de refação.
- Filtro por prioridade, incluindo `TODAS`.
- Resultado determinístico para listas vazias e entradas válidas.

**Testes previstos:**

- Cálculo de uma tarefa.
- Cálculo de múltiplas tarefas.
- Tarefas atrasadas e dentro do prazo.
- Agrupamento por prioridade.
- Taxa de refação.
- Filtro de prioridade.
- Lista vazia.
- Propagação de erros de validação.

**Implementação realizada:**

- Implementado `calculate_productivity_metrics` em
  `src/task_analyzer/core.py`.
- Adicionados cálculo de tempo médio em horas, taxa de atraso, taxa de
  retrabalho e agrupamento por prioridade.
- Adicionado filtro por `TODAS`, `None` ou prioridade específica.
- Definido retorno determinístico com zeros para entradas vazias.
- Adicionados testes unitários em `tests/test_core.py`.
- Atualizada a documentação do projeto.

### 4. Testes de integração — concluída

**Objetivo:** validar o fluxo completo entre entrada, validação e cálculo.

**Implementações previstas:**

- Criar cenários de integração sem persistência.
- Verificar a integração entre `utils.py` e `core.py`.
- Confirmar o formato final do dicionário de métricas.
- Confirmar que erros são explícitos e contextualizados.

**Testes previstos:**

- Fluxo completo com dados válidos.
- Fluxo com filtro de prioridade.
- Fluxo com dados inválidos.
- Fluxo com conjunto vazio.

**Implementação realizada:**

- Criado `tests/integration/test_task_analyzer.py`.
- Validado o fluxo completo entre entrada, validação e cálculo.
- Adicionados cenários com filtro de prioridade, dados inválidos e conjunto
  vazio.
- Confirmado que os testes não usam persistência em disco.
- Atualizada a documentação do projeto.
- Atualizada a versão do projeto de `0.3.0` para `0.4.0`.
- Criada a branch `feature/implement-integration-tests`.
- Nenhum arquivo foi deletado.

### 5. Pipeline CI/CD — concluída

**Objetivo:** automatizar a validação do projeto no GitHub Actions.

**Implementações previstas:**

- Criar `.github/workflows/ci.yml`.
- Configurar setup do ambiente Conda.
- Instalar as dependências declaradas.
- Executar testes unitários e de integração.
- Executar verificações de build e importação.
- Adicionar verificação de qualidade compatível com as regras do projeto,
  avaliando previamente qualquer dependência adicional.

**Implementação realizada:**

- Criado `.github/workflows/ci.yml`.
- Configurado o ambiente Conda a partir de `environment.yml`.
- Configurada execução da suíte Pytest em `push` e `pull_request` para as
  branches `main` e `master`.
- Configurada verificação de sintaxe com `compileall`.
- Restritas as permissões do workflow a leitura do conteúdo do repositório.
- Adicionadas as ferramentas `build` e `pylint` ao ambiente Conda.
- Configurada a construção dos artefatos com `python -m build`.
- Configurada a verificação de importação e da versão `0.5.0`.
- Configurado Pylint com nota mínima `8.0`.
- Atualizada a versão do projeto de `0.4.0` para `0.5.0`.
- Criada a branch `feature/complete-ci-pipeline`.
- Nenhum arquivo foi deletado.

### 6. Documentação e revisão final — concluída

**Objetivo:** consolidar o uso e verificar a conformidade final.

**Implementações previstas:**

- Atualizar o `README.md` com exemplos de uso aprovados.
- Documentar comandos de ambiente, testes e build.
- Conferir as assinaturas públicas contra a especificação.
- Conferir a cobertura dos requisitos.
- Executar a suíte completa de testes.
- Revisar compatibilidade com Python 3.11+.

**Implementação realizada:**

- Atualizado o `README.md` com instruções completas de ambiente, testes,
  build, importação e Pylint.
- Atualizada a especificação técnica com a árvore real do projeto e os testes
  unitários e de integração existentes.
- Conferidas as assinaturas públicas contra a implementação atual.
- Executados testes, compilação, build, importação e Pylint.
- Atualizada a versão do projeto de `0.5.0` para `0.6.0`.
- Atualizado o workflow para validar a versão `0.6.0`.
- Criada a branch `docs/finalize-documentation`.
- Nenhum arquivo foi deletado.

## Critérios de conclusão

O projeto será considerado concluído quando:

- O pacote puder ser instalado e importado pelo ambiente Conda.
- As métricas definidas na especificação estiverem implementadas.
- Os testes unitários e de integração estiverem aprovados.
- O pipeline CI/CD executar sem falhas.
- Não houver persistência de dados em disco ou banco.
- O código seguir as regras de tipagem, documentação, logging e estilo.
- O README refletir o comportamento implementado.
- A documentação de reprodução e os contratos refletirem o estado final.

## Governança das decisões

Decisões que alterem comportamento, contrato público, dependências, formato de
saída, estratégia de testes ou pipeline serão submetidas à aprovação antes da
implementação.
