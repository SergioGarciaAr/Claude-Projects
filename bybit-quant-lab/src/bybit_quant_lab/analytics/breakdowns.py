"""Desglose del rendimiento por dirección, motivo de salida, régimen, símbolo o temporalidad."""

from __future__ import annotations

import pandas as pd


def breakdown_trades(trades: pd.DataFrame, by: str) -> pd.DataFrame:
    """Agrega operaciones por la columna ``by`` (``side``, ``exit_reason``, ``regime``...)."""
    cols = ["trades", "net_pnl", "avg_net_pnl", "win_rate", "fees", "funding"]
    if trades.empty or by not in trades.columns:
        return pd.DataFrame(columns=cols)
    g = trades.groupby(by, dropna=False)
    out = pd.DataFrame(
        {
            "trades": g.size(),
            "net_pnl": g["net_pnl"].sum(),
            "avg_net_pnl": g["net_pnl"].mean(),
            "win_rate": g["net_pnl"].apply(lambda s: float((s > 0).mean())),
            "fees": g["fees"].sum(),
            "funding": g["funding"].sum(),
        }
    )
    return out.sort_values("net_pnl", ascending=False)
