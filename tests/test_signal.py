import asyncio
from decimal import Decimal

from src.accumulator import MessageAccumulator
from src.executor import PaperExecutor
from src.signal_parser import parse_deterministic


def test_parse_signal_fragments():
    text = "GOLD BUY entry 2345.50\nSL 2338.00\nTP1 2350.00\nTP2 2355.00\nTP3 2362.00"
    signal = parse_deterministic(text)
    assert signal.instrument == "GOLD"
    assert signal.direction == "BUY"
    assert signal.entry == Decimal("2345.50")
    assert signal.sl == Decimal("2338.00")
    assert signal.tp3 == Decimal("2362.00")


def test_accumulator_flushes_in_order():
    async def run():
        accumulator = MessageAccumulator()
        await accumulator.add("GOLD BUY")
        await accumulator.add("entry 2345.50")
        return await accumulator.flush()

    assert asyncio.run(run()) == "GOLD BUY entry 2345.50"


def test_paper_executor_does_not_require_live_broker():
    signal = parse_deterministic("GOLD BUY entry 2345.50 SL 2338.00 TP1 2350.00 TP3 2362.00")
    order = PaperExecutor().execute(signal)
    assert order.instrument == "GOLD"
    assert order.take_profit == Decimal("2362.00")
