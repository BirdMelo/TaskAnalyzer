"""Funções auxiliares de validação do TaskAnalyzer."""

import logging
from datetime import datetime
from typing import Any, Dict, List


LOGGER = logging.getLogger(__name__)
ALLOWED_PRIORITIES = frozenset({"ALTA", "MEDIA", "BAIXA"})
REQUIRED_FIELDS = (
    "started_at",
    "completed_at",
    "due_date",
    "priority",
    "rework_count",
)


def parse_datetime(value: Any, field_name: str) -> datetime:
    """Converte um valor ISO 8601 em um objeto datetime.

    Args:
        value: Valor a ser convertido.
        field_name: Nome do campo usado na mensagem de erro.

    Returns:
        Data e hora convertida.

    Raises:
        ValueError: Se o valor não for uma string ISO 8601 válida.
    """
    if not isinstance(value, str):
        message = f"{field_name} deve ser uma string ISO 8601."
        LOGGER.error(message)
        raise ValueError(message)

    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        message = f"{field_name} possui formato de data inválido: {value!r}."
        LOGGER.error(message)
        raise ValueError(message) from error


def validate_task(task: Dict[str, Any]) -> None:
    """Valida uma tarefa sem modificar seus dados.

    Args:
        task: Dicionário com os dados da tarefa.

    Raises:
        ValueError: Se a tarefa possuir campos ausentes ou inválidos.
    """
    if not isinstance(task, dict):
        message = "Cada tarefa deve ser um dicionário."
        LOGGER.error(message)
        raise ValueError(message)

    missing_fields = [field for field in REQUIRED_FIELDS if field not in task]
    if missing_fields:
        message = f"Tarefa sem campos obrigatórios: {', '.join(missing_fields)}."
        LOGGER.error(message)
        raise ValueError(message)

    started_at = parse_datetime(task["started_at"], "started_at")
    completed_at = parse_datetime(task["completed_at"], "completed_at")
    parse_datetime(task["due_date"], "due_date")

    if started_at.tzinfo != completed_at.tzinfo:
        message = "started_at e completed_at devem usar o mesmo fuso horário."
        LOGGER.error(message)
        raise ValueError(message)

    if started_at > completed_at:
        message = "started_at não pode ser posterior a completed_at."
        LOGGER.error(message)
        raise ValueError(message)

    priority = task["priority"]
    if priority not in ALLOWED_PRIORITIES:
        message = "priority deve ser ALTA, MEDIA ou BAIXA."
        LOGGER.error(message)
        raise ValueError(message)

    rework_count = task["rework_count"]
    if isinstance(rework_count, bool) or not isinstance(rework_count, int):
        message = "rework_count deve ser um inteiro não negativo."
        LOGGER.error(message)
        raise ValueError(message)
    if rework_count < 0:
        message = "rework_count deve ser um inteiro não negativo."
        LOGGER.error(message)
        raise ValueError(message)


def validate_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Valida uma lista de tarefas sem modificar seus dados.

    Args:
        tasks: Lista de tarefas a validar.

    Raises:
        ValueError: Se a entrada ou uma das tarefas for inválida.
    """
    if not isinstance(tasks, list):
        message = "tasks deve ser uma lista de dicionários."
        LOGGER.error(message)
        raise ValueError(message)

    for index, task in enumerate(tasks):
        try:
            validate_task(task)
        except ValueError as error:
            message = f"Tarefa na posição {index} inválida: {error}"
            LOGGER.error(message)
            raise ValueError(message) from error
