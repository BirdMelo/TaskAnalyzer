"""Métricas analíticas do TaskAnalyzer."""

import logging
from typing import Any, Dict, List, Optional

from task_analyzer.utils import ALLOWED_PRIORITIES, parse_datetime, validate_tasks


LOGGER = logging.getLogger(__name__)
ALL_PRIORITIES = ("ALTA", "MEDIA", "BAIXA")
ALL_PRIORITIES_FILTER = "TODAS"


def calculate_productivity_metrics(
    tasks: List[Dict[str, Any]],
    priority_filter: Optional[str] = "TODAS",
) -> Dict[str, Any]:
    """Calcula métricas de produtividade a partir de tarefas em memória.

    Args:
        tasks: Lista de dicionários contendo os dados das tarefas.
        priority_filter: Filtro opcional por prioridade. Use ``TODAS`` ou
            ``None`` para incluir todas as prioridades.

    Returns:
        Dicionário com ``average_completion_time``, ``delay_rate``,
        ``rework_rate`` e métricas agrupadas em ``by_priority``. Tempos são
        expressos em horas decimais e taxas em percentuais de 0 a 100.

    Raises:
        ValueError: Se as tarefas ou o filtro de prioridade forem inválidos.
    """
    validate_tasks(tasks)
    selected_priority = _validate_priority_filter(priority_filter)
    filtered_tasks = _filter_tasks(tasks, selected_priority)

    metrics = _calculate_metrics(filtered_tasks)
    metrics["by_priority"] = {
        priority: _calculate_metrics(
            [task for task in filtered_tasks if task["priority"] == priority]
        )
        for priority in ALL_PRIORITIES
    }
    LOGGER.info("Métricas calculadas para %d tarefas.", len(filtered_tasks))
    return metrics


def _validate_priority_filter(priority_filter: Optional[str]) -> Optional[str]:
    """Valida e normaliza o filtro de prioridade."""
    if priority_filter is None or priority_filter == ALL_PRIORITIES_FILTER:
        return None
    if priority_filter not in ALLOWED_PRIORITIES:
        message = (
            "priority_filter deve ser ALTA, MEDIA, BAIXA, TODAS ou None."
        )
        LOGGER.error(message)
        raise ValueError(message)
    return priority_filter


def _filter_tasks(
    tasks: List[Dict[str, Any]],
    priority_filter: Optional[str],
) -> List[Dict[str, Any]]:
    """Seleciona tarefas de acordo com o filtro de prioridade."""
    if priority_filter is None:
        return list(tasks)
    return [task for task in tasks if task["priority"] == priority_filter]


def _calculate_metrics(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula métricas para um subconjunto de tarefas."""
    if not tasks:
        return {
            "average_completion_time": 0.0,
            "delay_rate": 0.0,
            "rework_rate": 0.0,
        }

    completion_times = [
        _completion_time_in_hours(task) for task in tasks
    ]
    delayed_tasks = sum(
        _is_delayed(task) for task in tasks
    )
    reworked_tasks = sum(task["rework_count"] > 0 for task in tasks)
    task_count = len(tasks)

    return {
        "average_completion_time": sum(completion_times) / task_count,
        "delay_rate": delayed_tasks / task_count * 100,
        "rework_rate": reworked_tasks / task_count * 100,
    }


def _completion_time_in_hours(task: Dict[str, Any]) -> float:
    """Calcula o tempo de conclusão de uma tarefa em horas."""
    started_at = parse_datetime(task["started_at"], "started_at")
    completed_at = parse_datetime(task["completed_at"], "completed_at")
    return (completed_at - started_at).total_seconds() / 3600


def _is_delayed(task: Dict[str, Any]) -> bool:
    """Indica se uma tarefa foi concluída após o prazo."""
    completed_at = parse_datetime(task["completed_at"], "completed_at")
    due_date = parse_datetime(task["due_date"], "due_date")
    return completed_at > due_date
