"""Motor de backtesting determinista, vela a vela.

Orden de eventos dentro de cada vela ``i`` (índice = apertura de la vela):

1. Cambio de día UTC -> el gestor de riesgo reinicia la referencia diaria.
2. Funding: los pagos con marca de tiempo en ``(open[i-1], open[i]]`` se aplican a la
   posición mantenida al final de la vela ``i-1``, valorada a ``open[i]``.
3. Gap: si la apertura supera el stop/liquidación/objetivo, salida a la apertura.
4. Órdenes pendientes decididas al cierre de ``i-1``: primero salida, después entrada, ambas
   a ``open[i]`` con slippage adverso y comisión taker.
5. Intravela: stop/liquidación/objetivo con la regla *stop primero* (ver ``execution.fills``).
6. Cierre: valoración mark-to-market, registro de equity, límites de riesgo.
7. Trailing stop: se actualiza con el cierre y rige desde la vela siguiente.
8. Señal al cierre de ``i``: se programan órdenes para ``open[i+1]``. Nunca se ejecuta una
   señal al precio de la vela en que se generó.

Las entradas son *edge-triggered*: solo se abre posición cuando el objetivo de la estrategia
cambia a LONG/SHORT. Si un stop cierra la operación y la estrategia sigue en LONG, no se
reabre hasta una nueva transición. Las entradas rechazadas por riesgo no se difieren.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from bybit_quant_lab.backtesting.results import BacktestResult
from bybit_quant_lab.config.models import AppConfig
from bybit_quant_lab.execution.costs import CostModel
from bybit_quant_lab.execution.fills import ExitCheck, check_gap_exit, check_intrabar_exit
from bybit_quant_lab.portfolio.account import Account
from bybit_quant_lab.portfolio.position import Position, TradeRecord
from bybit_quant_lab.risk.instruments import InstrumentSpec, get_spec
from bybit_quant_lab.risk.limits import RiskManager
from bybit_quant_lab.risk.sizing import size_position
from bybit_quant_lab.strategies.base import SIGNAL_COLUMNS

FUNDING_INTERVAL = pd.Timedelta(hours=8)


@dataclass
class _PendingEntry:
    side: int
    stop_distance: float
    tp_distance: float | None
    trail_distance: float | None
    conviction: float
    regime: str


class BacktestEngine:
    """Simulador de un símbolo con una posición como máximo."""

    def __init__(
        self,
        config: AppConfig,
        symbol: str,
        timeframe: str,
        spec: InstrumentSpec | None = None,
    ) -> None:
        self.config = config
        self.symbol = symbol.upper()
        self.timeframe = timeframe
        self.spec = spec or get_spec(symbol)
        self.costs = CostModel.from_config(config.costs)

    # ------------------------------------------------------------------ API
    def run(
        self,
        data: pd.DataFrame,
        signals: pd.DataFrame,
        funding: pd.Series | None = None,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
        regime: pd.Series | None = None,
        label: str = "",
        params: dict[str, Any] | None = None,
    ) -> BacktestResult:
        """Simula ``[start, end]`` (inclusive). Las señales deben estar alineadas con ``data``."""
        self._check_inputs(data, signals)
        idx = pd.DatetimeIndex(data.index)
        i0 = 0 if start is None else int(idx.searchsorted(start, side="left"))
        i1 = len(idx) - 1 if end is None else int(idx.searchsorted(end, side="right")) - 1
        warnings: list[str] = []
        if i1 < i0:
            raise ValueError("El segmento solicitado no contiene velas")
        cfg = self.config
        acct = Account(cfg.backtest.initial_capital)
        risk = RiskManager(cfg.risk, cfg.backtest.initial_capital)
        o = data["open"].to_numpy(float)
        h = data["high"].to_numpy(float)
        low = data["low"].to_numpy(float)
        c = data["close"].to_numpy(float)
        sig = signals["signal"].to_numpy(np.int64)
        conv = signals["conviction"].to_numpy(float)
        stop_d = signals["stop_distance"].to_numpy(float)
        tp_d = signals["take_profit_distance"].to_numpy(float)
        tr_d = signals["trailing_distance"].to_numpy(float)
        regimes = (
            regime.reindex(idx).fillna("unknown").astype(str).to_numpy()
            if regime is not None
            else None
        )
        funding_by_bar, funding_ok, fw = self._map_funding(funding, idx, i0, i1)
        stamps = list(idx[i0 : i1 + 1])
        # Identificador de día UTC independiente de la resolución del índice (ns, us, ms...).
        day_ids = (
            idx.floor("D").as_unit("s").tz_convert(None).to_numpy().astype("int64") // 86_400
        ).tolist()
        warnings.extend(fw)

        trades: list[TradeRecord] = []
        rejected: list[dict[str, Any]] = []
        rows: list[tuple[float, float, float, float, float, bool]] = []
        pending_exit: str | None = None
        pending_entry: _PendingEntry | None = None
        prev_target = int(sig[i0 - 1]) if i0 > 0 else 0

        for i in range(i0, i1 + 1):
            ts = stamps[i - i0]
            risk.on_bar_open(ts, day_ids[i])
            pos = acct.position
            # 2. funding
            if pos is not None and i in funding_by_bar:
                payment = pos.side * pos.qty * o[i] * funding_by_bar[i]
                acct.cash -= payment
                acct.total_funding += payment
                pos.funding += payment
            # 3. gap
            if pos is not None:
                gap = check_gap_exit(
                    pos.side, o[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if gap is not None:
                    trades.append(self._close(acct, risk, gap, i, ts))
                    pending_exit = None
            # 4. pending orders at open
            if pending_exit is not None and acct.position is not None:
                trades.append(self._close(acct, risk, ExitCheck(o[i], pending_exit), i, ts))
            pending_exit = None
            if pending_entry is not None and acct.position is None:
                rej = self._open(acct, pending_entry, o[i], i, ts)
                if rej:
                    rejected.append({"time": str(ts), "side": pending_entry.side, "reason": rej})
            pending_entry = None
            # 5. intrabar
            pos = acct.position
            if pos is not None:
                hit = check_intrabar_exit(
                    pos.side, h[i], low[i], pos.stop, pos.take_profit, pos.liquidation_price
                )
                if hit is not None:
                    trades.append(self._close(acct, risk, hit, i, ts))
            # 6. close / mark to market
            pos = acct.position
            unreal = pos.unrealized(c[i]) if pos else 0.0
            equity = acct.cash + unreal
            rows.append(
                (
                    equity,
                    acct.cash,
                    unreal,
                    pos.side * pos.qty if pos else 0.0,
                    acct.used_margin,
                    pos is not None,
                )
            )
            force_close = risk.on_bar_close(ts, equity)
            # 7. trailing
            if pos is not None:
                pos.update_trailing(c[i])
            if i == i1:
                break
            # 8. decision at close
            target = int(sig[i])
            if force_close and acct.position is not None:
                pending_exit = "risk_limit_close"
            elif acct.position is not None and target != acct.position.side:
                pending_exit = "signal_exit" if target == 0 else "signal_reverse"
            is_edge = target not in (0, prev_target)
            prev_target = target
            if is_edge:
                can_reverse = acct.position is None or (
                    pending_exit is not None and cfg.execution.allow_reversal
                )
                allowed, reason = risk.can_open(i)
                if not can_reverse:
                    rejected.append({"time": str(ts), "side": target, "reason": "position_open"})
                elif not allowed:
                    rejected.append({"time": str(ts), "side": target, "reason": reason})
                else:
                    pending_entry = _PendingEntry(
                        side=target,
                        stop_distance=float(stop_d[i]),
                        tp_distance=_nan_to_none(tp_d[i]),
                        trail_distance=_nan_to_none(tr_d[i]),
                        conviction=float(conv[i]),
                        regime=str(regimes[i]) if regimes is not None else "",
                    )
        # final
        if acct.position is not None and cfg.execution.close_at_end:
            trades.append(self._close(acct, risk, ExitCheck(c[i1], "end_of_data"), i1, idx[i1]))
            final_equity = acct.cash
            rows[-1] = (final_equity, acct.cash, 0.0, 0.0, 0.0, rows[-1][5])

        equity_df = pd.DataFrame(
            rows,
            index=idx[i0 : i1 + 1],
            columns=["equity", "cash", "unrealized", "position", "margin_used", "in_position"],
        )
        peak = equity_df["equity"].cummax()
        equity_df["drawdown"] = equity_df["equity"] / peak - 1
        trades_df = pd.DataFrame([t.to_dict() for t in trades])
        if trades_df.empty:
            trades_df = pd.DataFrame(columns=list(TradeRecord.__dataclass_fields__))
        if not self.spec.verified:
            warnings.append(
                f"Especificaciones de {self.symbol} no verificadas con instruments-info "
                "(valores de referencia)."
            )
        totals = {
            "fees": acct.total_fees,
            "slippage": acct.total_slippage,
            "funding": acct.total_funding,
            "traded_notional": acct.traded_notional,
        }
        return BacktestResult(
            label=label,
            symbol=self.symbol,
            timeframe=self.timeframe,
            initial_capital=cfg.backtest.initial_capital,
            equity=equity_df,
            trades=trades_df,
            risk_events=[e.to_dict() for e in risk.events],
            rejected_signals=rejected,
            totals=totals,
            funding_applied=funding_ok,
            warnings=warnings,
            params=dict(params or {}),
        )

    # ------------------------------------------------------------- helpers
    @staticmethod
    def _check_inputs(data: pd.DataFrame, signals: pd.DataFrame) -> None:
        missing = [c for c in SIGNAL_COLUMNS if c not in signals.columns]
        if missing:
            raise ValueError(f"Faltan columnas de señal: {missing}")
        if not data.index.equals(signals.index):
            raise ValueError("Las señales deben tener exactamente el mismo índice que los datos")
        if data.empty:
            raise ValueError("No hay datos para simular")
        if data[["open", "high", "low", "close"]].isna().any().any():
            raise ValueError("Los datos contienen precios NaN; límpialos antes de simular")

    def _map_funding(
        self, funding: pd.Series | None, idx: pd.DatetimeIndex, i0: int, i1: int
    ) -> tuple[dict[int, float], bool, list[str]]:
        if not self.config.costs.use_funding:
            return {}, False, ["Funding desactivado en la configuración."]
        if funding is None or funding.empty:
            return (
                {},
                False,
                [
                    "Sin datos históricos de funding: no se aplica (no se simula). El resultado "
                    "neto excluye el coste/ingreso de funding."
                ],
            )
        seg_start, seg_end = idx[i0], idx[i1]
        warnings = []
        if funding.index.min() > seg_start + FUNDING_INTERVAL or funding.index.max() < (
            seg_end - FUNDING_INTERVAL
        ):
            warnings.append("El funding disponible no cubre todo el período simulado.")
        out: dict[int, float] = {}
        positions = idx.searchsorted(pd.DatetimeIndex(funding.index), side="left")
        for j, rate in zip(positions, funding.to_numpy(float), strict=True):
            if i0 < j <= i1 and not np.isnan(rate):
                out[int(j)] = out.get(int(j), 0.0) + float(rate)
        return out, True, warnings

    def _open(
        self, acct: Account, pe: _PendingEntry, ref_price: float, i: int, ts: pd.Timestamp
    ) -> str | None:
        cfg = self.config
        fill = self.costs.fill_price(ref_price, pe.side)
        equity = acct.equity(ref_price)
        sizing = size_position(
            equity,
            acct.used_margin,
            fill,
            pe.stop_distance,
            cfg.risk,
            cfg.execution,
            cfg.costs,
            self.spec,
        )
        if sizing.qty <= 0:
            return sizing.reason
        qty = sizing.qty
        notional = qty * fill
        fee = self.costs.fee(notional)
        lev = cfg.execution.leverage
        mmr = cfg.execution.maintenance_margin_rate
        liq = None
        if cfg.execution.simulate_liquidation:
            liq = fill * (1 - 1 / lev + mmr) if pe.side > 0 else fill * (1 + 1 / lev - mmr)
        acct.cash -= fee
        acct.total_fees += fee
        acct.total_slippage += abs(fill - ref_price) * qty
        acct.traded_notional += notional
        acct.position = Position(
            side=pe.side,
            qty=qty,
            entry_price=fill,
            entry_time=ts,
            entry_bar=i,
            stop=fill - pe.side * pe.stop_distance,
            take_profit=fill + pe.side * pe.tp_distance if pe.tp_distance else None,
            trailing_distance=pe.trail_distance,
            liquidation_price=liq,
            margin=notional / lev,
            entry_fee=fee,
            entry_slippage=abs(fill - ref_price) * qty,
            conviction=pe.conviction,
            extreme=fill,
            equity_at_entry=equity,
            regime=pe.regime,
        )
        return None

    def _close(
        self, acct: Account, risk: RiskManager, ex: ExitCheck, i: int, ts: pd.Timestamp
    ) -> TradeRecord:
        pos = acct.position
        assert pos is not None
        if ex.reason.startswith("liquidation"):
            # Margen aislado: se pierde el margen inicial completo (aproximación).
            fill = pos.entry_price - pos.side * pos.margin / pos.qty
        else:
            fill = self.costs.fill_price(ex.price, -pos.side)
        exit_slip = abs(fill - ex.price) * pos.qty
        exit_fee = self.costs.fee(pos.qty * fill)
        price_pnl = pos.side * (fill - pos.entry_price) * pos.qty
        acct.cash += price_pnl - exit_fee
        acct.realized_pnl += price_pnl
        acct.total_fees += exit_fee
        acct.total_slippage += exit_slip
        acct.traded_notional += pos.qty * fill
        entry_ref = pos.entry_price - pos.side * pos.entry_slippage / pos.qty
        gross = pos.side * (ex.price - entry_ref) * pos.qty
        fees = pos.entry_fee + exit_fee
        net = price_pnl - fees - pos.funding
        eq_entry = pos.equity_at_entry or acct.initial_capital
        record = TradeRecord(
            symbol=self.symbol,
            side="LONG" if pos.side > 0 else "SHORT",
            entry_time=pos.entry_time,
            exit_time=ts,
            entry_bar=pos.entry_bar,
            exit_bar=i,
            qty=pos.qty,
            entry_price=pos.entry_price,
            exit_price=fill,
            gross_pnl=gross,
            fees=fees,
            slippage_cost=pos.entry_slippage + exit_slip,
            funding=pos.funding,
            net_pnl=net,
            return_on_equity=net / eq_entry if eq_entry else 0.0,
            bars_held=i - pos.entry_bar + 1,
            exit_reason=ex.reason,
            conviction=pos.conviction,
            equity_at_entry=eq_entry,
            regime=pos.regime,
        )
        acct.position = None
        risk.on_trade_closed(i, ts, net)
        return record


def _nan_to_none(x: float) -> float | None:
    return None if x is None or np.isnan(x) or x <= 0 else float(x)


def run_backtest(
    data: pd.DataFrame,
    signals: pd.DataFrame,
    config: AppConfig,
    symbol: str,
    timeframe: str,
    **kwargs: Any,
) -> BacktestResult:
    """Atajo funcional para ``BacktestEngine(...).run(...)``."""
    spec = kwargs.pop("spec", None)
    return BacktestEngine(config, symbol, timeframe, spec).run(data, signals, **kwargs)
