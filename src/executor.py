"""Safe execution abstraction.

The public project only provides a paper/simulation executor. It never sends
orders to MetaTrader 5 or any live brokerage account.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import TradeSignal


@dataclass(frozen=True)
class SimulatedOrder:
    instrument: str
    direction: str
    entry: Decimal
    stop_loss: Decimal
    take_profit: Decimal | None


class PaperExecutor:
    def execute(self, signal: TradeSignal) -> SimulatedOrder:
        if signal.entry is None or signal.sl is None:
            raise ValueError("Signal must contain entry and stop-loss values")
        return SimulatedOrder(
            instrument=signal.instrument,
            direction=signal.direction,
            entry=signal.entry,
            stop_loss=signal.sl,
            take_profit=signal.tp3 or signal.tp2 or signal.tp1,
        )
