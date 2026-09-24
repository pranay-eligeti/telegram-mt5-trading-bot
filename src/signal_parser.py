"""Deterministic signal parser with optional Claude extraction.

The public repository never sends messages to a broker. It focuses on the
engineering problem of normalizing semi-structured messages into a typed event.
"""

from __future__ import annotations

import json
import os
import re
from decimal import Decimal
from typing import Any

from anthropic import Anthropic

from .models import TradeSignal


NUMBER = r"([0-9]+(?:[.,][0-9]+)?)"


def _number(pattern: str, text: str) -> Decimal | None:
    match = re.search(pattern, text, re.I)
    if not match:
        return None
    return Decimal(match.group(1).replace(",", ""))


def parse_deterministic(text: str) -> TradeSignal:
    raw = " ".join(text.strip().split())
    direction_match = re.search(r"\b(BUY|SELL)\b", raw, re.I)
    instrument_match = re.search(r"\b(GOLD|XAUUSD|BTCUSDT|BTC/USD|BTC)\b", raw, re.I)

    if not direction_match or not instrument_match:
        raise ValueError("Could not identify direction and instrument")

    instrument = instrument_match.group(1).upper().replace("BTC/USD", "BTCUSDT")
    direction = direction_match.group(1).upper()

    entry = _number(rf"(?:ENTRY|AT|ENTRY\s*ZONE)\s*[:=-]?\s*{NUMBER}", raw)
    sl = _number(rf"(?:SL|STOP\s*LOSS)\s*[:=-]?\s*{NUMBER}", raw)
    tp1 = _number(rf"(?:TP1|TARGET\s*1)\s*[:=-]?\s*{NUMBER}", raw)
    tp2 = _number(rf"(?:TP2|TARGET\s*2)\s*[:=-]?\s*{NUMBER}", raw)
    tp3 = _number(rf"(?:TP3|TARGET\s*3)\s*[:=-]?\s*{NUMBER}", raw)

    return TradeSignal(
        instrument=instrument,
        direction=direction,
        entry=entry,
        tp1=tp1,
        tp2=tp2,
        tp3=tp3,
        sl=sl,
        source_text=raw,
    )


def parse_with_claude(text: str, model: str | None = None) -> TradeSignal:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured")

    client = Anthropic(api_key=api_key)
    model_name = model or os.environ.get("PARSER_MODEL", "claude-3-5-sonnet-latest")
    prompt = (
        "Convert this trading signal into JSON with keys instrument, direction, "
        "entry, tp1, tp2, tp3, sl. Use null for missing values. Never invent "
        "prices. Normalize direction to BUY or SELL.\n\n"
        f"Message:\n{text}"
    )
    response = client.messages.create(
        model=model_name,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    block = response.content[0]
    raw_json = getattr(block, "text", str(block)).strip()
    data: dict[str, Any] = json.loads(raw_json)
    data["source_text"] = text
    return TradeSignal.model_validate(data)
