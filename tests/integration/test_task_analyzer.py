"""Testes de integração do fluxo completo do TaskAnalyzer."""

# Os dados repetidos representam fixtures independentes dos testes unitários.
# pylint: disable=duplicate-code
import pytest

from task_analyzer.core import calculate_productivity_metrics


def build_task(
    priority: str,
    completed_at: str,
    due_date: str,
    rework_count: int,
) -> dict[str, object]:
    """Cria uma tarefa para os cenários de integração."""
    return {
        "started_at": "2026-01-01T08:00:00",
        "completed_at": completed_at,
        "due_date": due_date,
        "priority": priority,
        "rework_count": rework_count,
    }


def test_complete_flow_returns_global_and_priority_metrics() -> None:
    """Integra entrada, validação e cálculo das métricas."""
    tasks = [
        build_task(
            priority="ALTA",
            completed_at="2026-01-01T10:00:00",
            due_date="2026-01-01T12:00:00",
            rework_count=0,
        ),
        build_task(
            priority="MEDIA",
            completed_at="2026-01-01T14:00:00",
            due_date="2026-01-01T13:00:00",
            rework_count=1,
        ),
    ]

    result = calculate_productivity_metrics(tasks)

    assert result["average_completion_time"] == 4.0
    assert result["delay_rate"] == 50.0
    assert result["rework_rate"] == 50.0
    assert result["by_priority"]["MEDIA"]["delay_rate"] == 100.0


def test_complete_flow_applies_priority_filter() -> None:
    """Integra a validação ao cálculo filtrado por prioridade."""
    tasks = [
        build_task("ALTA", "2026-01-01T10:00:00", "2026-01-01T12:00:00", 0),
        build_task("BAIXA", "2026-01-01T16:00:00", "2026-01-01T15:00:00", 2),
    ]

    result = calculate_productivity_metrics(tasks, priority_filter="BAIXA")

    assert result["average_completion_time"] == 8.0
    assert result["delay_rate"] == 100.0
    assert result["rework_rate"] == 100.0
    assert result["by_priority"]["ALTA"]["average_completion_time"] == 0.0


def test_complete_flow_rejects_invalid_task() -> None:
    """Interrompe o fluxo quando a validação encontra dados inválidos."""
    invalid_tasks = [
        build_task("ALTA", "2026-01-01T10:00:00", "2026-01-01T12:00:00", 0),
        build_task(
            "URGENTE",
            "2026-01-01T10:00:00",
            "2026-01-01T12:00:00",
            0,
        ),
    ]

    with pytest.raises(ValueError, match="posição 1"):
        calculate_productivity_metrics(invalid_tasks)


def test_complete_flow_handles_empty_input() -> None:
    """Mantém o contrato de saída para um conjunto vazio."""
    result = calculate_productivity_metrics([])

    assert result == {
        "average_completion_time": 0.0,
        "delay_rate": 0.0,
        "rework_rate": 0.0,
        "by_priority": {
            "ALTA": {
                "average_completion_time": 0.0,
                "delay_rate": 0.0,
                "rework_rate": 0.0,
            },
            "MEDIA": {
                "average_completion_time": 0.0,
                "delay_rate": 0.0,
                "rework_rate": 0.0,
            },
            "BAIXA": {
                "average_completion_time": 0.0,
                "delay_rate": 0.0,
                "rework_rate": 0.0,
            },
        },
    }
