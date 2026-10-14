"""Harness avaliativo para os cenários funcionais do TaskAnalyzer."""

import pytest

from task_analyzer.core import calculate_productivity_metrics

# O helper repete o formato do cenário exigido pelo contrato avaliativo.
# pylint: disable=duplicate-code


def build_task(
    priority: str = "ALTA",
    completed_at: str = "2026-01-01T10:00:00",
    due_date: str = "2026-01-01T12:00:00",
    rework_count: int = 0,
) -> dict[str, object]:
    """Cria uma tarefa válida para os cenários avaliativos."""
    return {
        "started_at": "2026-01-01T08:00:00",
        "completed_at": completed_at,
        "due_date": due_date,
        "priority": priority,
        "rework_count": rework_count,
    }


def test_scenario_1_calculates_productivity_metrics() -> None:
    """Cenário 1: calcula métricas globais e segmentadas."""
    result = calculate_productivity_metrics(
        [
            build_task(),
            build_task(
                priority="MEDIA",
                completed_at="2026-01-01T14:00:00",
                due_date="2026-01-01T13:00:00",
                rework_count=1,
            ),
        ]
    )

    assert result["average_completion_time"] == 4.0
    assert result["delay_rate"] == 50.0
    assert result["rework_rate"] == 50.0
    assert result["by_priority"]["MEDIA"]["delay_rate"] == 100.0


def test_scenario_2_filters_by_priority() -> None:
    """Cenário 2: limita o cálculo à prioridade informada."""
    result = calculate_productivity_metrics(
        [
            build_task(),
            build_task(
                priority="BAIXA",
                completed_at="2026-01-01T16:00:00",
                due_date="2026-01-01T15:00:00",
                rework_count=2,
            ),
        ],
        priority_filter="BAIXA",
    )

    assert result["average_completion_time"] == 8.0
    assert result["delay_rate"] == 100.0
    assert result["rework_rate"] == 100.0
    assert result["by_priority"]["ALTA"]["average_completion_time"] == 0.0


def test_harness_handles_empty_input() -> None:
    """Caso de borda: mantém o contrato numérico para entrada vazia."""
    result = calculate_productivity_metrics([])

    assert result["average_completion_time"] == 0.0
    assert result["delay_rate"] == 0.0
    assert result["rework_rate"] == 0.0
    assert set(result["by_priority"]) == {"ALTA", "MEDIA", "BAIXA"}


def test_harness_rejects_invalid_task() -> None:
    """Caso de borda: rejeita uma prioridade fora do contrato."""
    invalid_task = build_task(priority="URGENTE")

    with pytest.raises(ValueError, match="posição 0"):
        calculate_productivity_metrics([invalid_task])


def test_harness_rejects_invalid_filter() -> None:
    """Caso de borda: rejeita um filtro de prioridade desconhecido."""
    with pytest.raises(ValueError, match="priority_filter"):
        calculate_productivity_metrics([], priority_filter="URGENTE")
