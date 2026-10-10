"""Registro reproducible de experimentos (JSON Lines) y protección del período de test.

Cada configuración evaluada se registra con su segmento, parámetros, hash de datos y
métricas, lo que permite contar el número de configuraciones probadas (necesario para
corregir por pruebas múltiples). El período de test final solo puede evaluarse una vez por
selección congelada; repetirlo exige ``allow_repeat`` y queda marcado.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class ExperimentLog:
    """Registro append-only en ``path``."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: dict[str, Any]) -> None:
        """Añade un registro con marca temporal UTC."""
        rec = {"logged_at": datetime.now(UTC).isoformat(), **record}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, default=str, sort_keys=True) + "\n")

    def records(self) -> list[dict[str, Any]]:
        """Todos los registros."""
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def count(self, kind: str | None = None, data_hash: str | None = None) -> int:
        """Número de configuraciones registradas (filtrables por tipo y datos)."""
        return sum(
            1
            for r in self.records()
            if (kind is None or r.get("kind") == kind)
            and (data_hash is None or r.get("data_hash") == data_hash)
        )

    def count_distinct_configs(
        self, data_hash: str, segment: str = "validation", cost_mode: str = "net"
    ) -> int:
        """Configuraciones distintas (candidato + parámetros) evaluadas en ``segment``.

        Es el número de pruebas que se usa para deflactar el Sharpe: incluye todas las
        ejecuciones registradas sobre los mismos datos, no solo la actual.
        """
        keys = {
            json.dumps([r.get("candidate"), r.get("params")], sort_keys=True, default=str)
            for r in self.records()
            if r.get("kind") == "evaluation"
            and r.get("data_hash") == data_hash
            and r.get("segment") == segment
            and r.get("cost_mode") == cost_mode
        }
        return len(keys)


class FinalTestAlreadyEvaluatedError(RuntimeError):
    """El período de test ya fue evaluado para esta selección."""


def guard_final_test(
    log: ExperimentLog,
    selection_id: str,
    allow_repeat: bool,
    data_hash: str | None = None,
    test_segment: dict[str, Any] | None = None,
) -> bool:
    """Comprueba si el período de test ya se usó. Devuelve ``True`` si es repetición.

    Bloquea tanto la misma selección como **cualquier otra** evaluada sobre los mismos datos
    y el mismo período de test: probar varias selecciones contra el test y quedarse con la
    mejor equivale a seleccionar con el test.
    """

    def same_period(r: dict[str, Any]) -> bool:
        return (
            data_hash is not None
            and r.get("data_hash") == data_hash
            and (test_segment is None or r.get("test_segment") in (None, test_segment))
        )

    done = [
        r
        for r in log.records()
        if r.get("kind") == "final_test"
        and (r.get("selection_id") == selection_id or same_period(r))
    ]
    if done and not allow_repeat:
        raise FinalTestAlreadyEvaluatedError(
            f"El período de test de estos datos ya se evaluó el {done[0]['logged_at']} "
            f"(selección {done[0].get('selection_id')}). Evaluar otra selección o la misma tras "
            "cambios invalidaría la independencia del test. Usa --allow-repeat solo si "
            "entiendes la consecuencia; el informe lo marcará como no independiente."
        )
    return bool(done)
