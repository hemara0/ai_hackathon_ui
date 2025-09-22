"""Utility helpers for validating JSON payloads supplied through the UI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ValidationResult:
    """Structured result returned after validating a JSON string."""

    is_valid: bool
    message: str
    payload: Optional[Any] = None


def validate_json(raw_text: str) -> ValidationResult:
    """Validate that *raw_text* contains valid JSON.

    Returns a :class:`ValidationResult` detailing whether the input is valid
    together with either the parsed payload or an error message with location
    context when available.
    """

    if raw_text is None or not raw_text.strip():
        return ValidationResult(
            is_valid=False,
            message="No JSON content provided. Paste a payload before validating.",
        )

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        location = f"line {exc.lineno}, column {exc.colno}"
        return ValidationResult(
            is_valid=False,
            message=f"Invalid JSON: {exc.msg} at {location}.",
        )
    except Exception as exc:  # pragma: no cover - defensive catch-all
        return ValidationResult(
            is_valid=False,
            message=f"Unexpected error while validating JSON: {exc}",
        )

    return ValidationResult(is_valid=True, message="JSON is valid.", payload=parsed)


__all__ = ["ValidationResult", "validate_json"]
