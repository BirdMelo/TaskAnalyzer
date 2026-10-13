# TaskAnalyzer

Módulo Python para análise de produtividade de tarefas em memória, conforme a
especificação técnica em [`specs/task_analyzer_spec.md`](specs/task_analyzer_spec.md).

## Requisitos

- Conda ou Anaconda
- Python 3.11 ou superior

## Configuração do ambiente

Crie o ambiente Conda definido no repositório:

```bash
conda env create -f environment.yml
conda activate task-analyzer
```

Se o ambiente já existir, atualize as dependências com:

```bash
conda env update -f environment.yml --prune
```

## Execução dos testes

Com o ambiente ativado, execute:

```bash
pytest
```

A configuração do projeto utiliza o layout `src/`, portanto o pacote
`task_analyzer` é carregado a partir de `src/task_analyzer`.

## Estrutura do projeto

```text
BootCampIII-TaskAnalyzer/
├── .github/workflows/       # Pipeline CI/CD (implementação planejada)
├── environment.yml          # Ambiente Conda reproduzível
├── specs/                   # Especificação técnica
├── src/task_analyzer/       # Pacote principal
│   ├── core.py              # Métricas analíticas
│   └── utils.py             # Validações e auxiliares
└── tests/                   # Testes automatizados
```

## Plano de implementação

As etapas serão executadas individualmente, mediante autorização:

1. **Build e estrutura inicial:** concluída nesta etapa.
2. **Validações e utilitários:** implementar validação tipada de tarefas e
   respectivos testes unitários.
3. **Métricas analíticas:** implementar o contrato de
   `calculate_productivity_metrics` e testes unitários.
4. **Integração:** adicionar cenários de integração sem persistência em disco.
5. **Pipeline:** configurar GitHub Actions com Conda, Pytest e verificações de
   qualidade.
6. **Documentação e revisão final:** consolidar uso, cobertura e critérios de
   aceitação.

Nenhuma etapa posterior altera o contrato público sem autorização explícita.