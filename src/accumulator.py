"""Small async message accumulator for bursty event streams."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class MessageAccumulator:
    window_seconds: float = 2.0
    _messages: list[str] = field(default_factory=list)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def add(self, message: str) -> None:
        async with self._lock:
            if message.strip():
                self._messages.append(message.strip())

    async def flush(self) -> str:
        async with self._lock:
            combined = " ".join(self._messages)
            self._messages.clear()
            return combined
