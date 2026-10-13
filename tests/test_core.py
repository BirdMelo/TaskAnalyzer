"""Testes unitários das métricas analíticas do TaskAnalyzer."""

import pytest

from task_analyzer.core import calculate_productivity_metrics


def task(
    priority: str = "ALTA",
    completed_at: str = "2026-01-01T10:00:00",
    due_date: str = "2026-01-01T12:00:00",
    rework_count: int = 0,
) -> dict[str, object]:
    """Cria uma tarefa válida para os testes."""
    return {
        "started_at": "2026-01-01T08:00:00",
        "completed_at": completed_at,
        "due_date": due_date,
        "priority": priority,
        "rework_count": rework_count,
    }


def test_calculate_metrics_returns_global_values() -> None:
    """Calcula tempo médio, atraso e retrabalho."""
    metrics = calculate_productivity_metrics(
        [
            task(),
            task(
                priority="MEDIA",
                completed_at="2026-01-01T14:00:00",
                due_date="2026-01-01T13:00:00",
                rework_count=1,
            ),
        ]
    )

    assert metrics["average_completion_time"] == 4.0
    assert metrics["delay_rate"] == 50.0
    assert metrics["rework_rate"] == 50.0


def test_calculate_metrics_groups_by_priority() -> None:
    """Agrupa o tempo médio e as taxas por prioridade."""
    metrics = calculate_productivity_metrics(
        [task("ALTA"), task("BAIXA", rework_count=1)]
    )

    assert metrics["by_priority"]["ALTA"] == {
        "average_completion_time": 2.0,
        "delay_rate": 0.0,
        "rework_rate": 0.0,
    }
    assert metrics["by_priority"]["MEDIA"] == {
        "average_completion_time": 0.0,
        "delay_rate": 0.0,
        "rework_rate": 0.0,
    }


def test_calculate_metrics_filters_priority() -> None:
    """Calcula as métricas somente para a prioridade selecionada."""
    metrics = calculate_productivity_metrics(
        [task("ALTA"), task("BAIXA", rework_count=1)],
        priority_filter="BAIXA",
    )

    assert metrics["average_completion_time"] == 2.0
    assert metrics["delay_rate"] == 0.0
    assert metrics["rework_rate"] == 100.0
    assert metrics["by_priority"]["ALTA"]["average_completion_time"] == 0.0


def test_calculate_metrics_empty_input_returns_zeros() -> None:
    """Retorna zeros para uma lista vazia."""
    metrics = calculate_productivity_metrics([])

    assert metrics["average_completion_time"] == 0.0
    assert metrics["delay_rate"] == 0.0
    assert metrics["rework_rate"] == 0.0
    assert set(metrics["by_priority"]) == {"ALTA", "MEDIA", "BAIXA"}


def test_calculate_metrics_rejects_invalid_priority_filter() -> None:
    """Rejeita filtros de prioridade desconhecidos."""
    with pytest.raises(ValueError, match="priority_filter"):
        calculate_productivity_metrics([], priority_filter="URGENTE")


def test_calculate_metrics_propagates_task_validation_errors() -> None:
    """Propaga erros das validações de tarefas."""
    invalid_task = task()
    invalid_task["rework_count"] = -1

    with pytest.raises(ValueError, match="rework_count"):
        calculate_productivity_metrics([invalid_task])
