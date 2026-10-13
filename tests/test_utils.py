"""Testes unitários para os utilitários do TaskAnalyzer."""

from copy import deepcopy

import pytest

from task_analyzer.utils import parse_datetime, validate_task, validate_tasks


def valid_task() -> dict[str, object]:
    """Retorna uma tarefa válida para os testes."""
    return {
        "started_at": "2026-01-01T08:00:00",
        "completed_at": "2026-01-01T10:00:00",
        "due_date": "2026-01-01T12:00:00",
        "priority": "ALTA",
        "rework_count": 0,
    }


def test_parse_datetime_returns_datetime() -> None:
    """Converte uma data ISO 8601 válida."""
    parsed = parse_datetime("2026-01-01T08:00:00", "started_at")

    assert parsed.year == 2026
    assert parsed.hour == 8


@pytest.mark.parametrize("field", ["started_at", "completed_at", "due_date"])
def test_parse_datetime_rejects_invalid_values(field: str) -> None:
    """Rejeita valores que não são strings de data válidas."""
    with pytest.raises(ValueError, match=field):
        parse_datetime(42, field)


def test_validate_task_accepts_valid_task() -> None:
    """Aceita uma tarefa que atende ao contrato."""
    validate_task(valid_task())


def test_validate_task_does_not_mutate_task() -> None:
    """Preserva os dados recebidos durante a validação."""
    task = valid_task()
    original = deepcopy(task)

    validate_task(task)

    assert task == original


@pytest.mark.parametrize(
    "field",
    ["started_at", "completed_at", "due_date", "priority", "rework_count"],
)
def test_validate_task_rejects_missing_required_field(field: str) -> None:
    """Rejeita campos obrigatórios ausentes."""
    task = valid_task()
    del task[field]

    with pytest.raises(ValueError, match=field):
        validate_task(task)


def test_validate_task_rejects_inverted_interval() -> None:
    """Rejeita um início posterior à conclusão."""
    task = valid_task()
    task["started_at"] = "2026-01-01T11:00:00"

    with pytest.raises(ValueError, match="started_at"):
        validate_task(task)


def test_validate_task_rejects_invalid_priority() -> None:
    """Rejeita prioridades fora do contrato."""
    task = valid_task()
    task["priority"] = "URGENTE"

    with pytest.raises(ValueError, match="priority"):
        validate_task(task)


@pytest.mark.parametrize("value", [-1, 1.5, True])
def test_validate_task_rejects_invalid_rework_count(value: object) -> None:
    """Rejeita contagens de retrabalho inválidas."""
    task = valid_task()
    task["rework_count"] = value

    with pytest.raises(ValueError, match="rework_count"):
        validate_task(task)


def test_validate_tasks_reports_task_index() -> None:
    """Inclui a posição da tarefa inválida no erro."""
    task = valid_task()
    task["priority"] = "URGENTE"

    with pytest.raises(ValueError, match="posição 0"):
        validate_tasks([task])
