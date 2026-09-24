"""Domain models for normalized trade-signal events."""

from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, Field


class TradeSignal(BaseModel):
    instrument: str
    direction: str
    entry: Decimal | None = None
    tp1: Decimal | None = None
    tp2: Decimal | None = None
    tp3: Decimal | None = None
    sl: Decimal | None = None
    source_text: str = Field(min_length=1)

    @property
    def is_complete(self) -> bool:
        return all(
            value is not None
            for value in (self.instrument, self.direction, self.entry, self.sl)
        )
