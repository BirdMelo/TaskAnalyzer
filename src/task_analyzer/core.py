"""Métricas analíticas do TaskAnalyzer."""

from typing import Any, Dict, List, Optional


def calculate_productivity_metrics(
    tasks: List[Dict[str, Any]],
    priority_filter: Optional[str] = "TODAS",
) -> Dict[str, Any]:
    """Calcula métricas de produtividade a partir de tarefas em memória.

    Args:
        tasks: Lista de dicionários contendo os dados das tarefas.
        priority_filter: Filtro opcional por prioridade.

    Returns:
        Dicionário com as métricas calculadas.

    Raises:
        NotImplementedError: Enquanto a implementação analítica não for
            autorizada e concluída em uma etapa posterior.
    """
    raise NotImplementedError(
        "A implementação das métricas será entregue na etapa analítica."
    )
