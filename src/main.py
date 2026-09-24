"""CLI for the public signal parsing and simulation demo."""

from __future__ import annotations

import argparse
from pathlib import Path

from .accumulator import MessageAccumulator
from .executor import PaperExecutor
from .signal_parser import parse_deterministic


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a synthetic signal and simulate an order.")
    parser.add_argument("--input", required=True, help="Text file containing signal fragments")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    accumulator = MessageAccumulator()

    import asyncio

    async def collect() -> str:
        for line in text.splitlines():
            await accumulator.add(line)
        return await accumulator.flush()

    combined = asyncio.run(collect())
    signal = parse_deterministic(combined)
    simulated = PaperExecutor().execute(signal)
    print(simulated)


if __name__ == "__main__":
    main()
