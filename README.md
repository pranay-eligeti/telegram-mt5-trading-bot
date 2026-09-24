# 📈 Event-Driven Trading Signal Parser

> A sanitized, runnable Python portfolio project demonstrating bursty message accumulation, semi-structured signal parsing, typed events, optional LLM extraction, and paper-only execution.

[![Python CI](https://github.com/pranay-eligeti/telegram-mt5-trading-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/pranay-eligeti/telegram-mt5-trading-bot/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Pydantic](https://img.shields.io/badge/Pydantic-typed%20models-E92063)
![Claude](https://img.shields.io/badge/Claude-optional%20LLM-purple)

## What this repository demonstrates

I have worked on event-driven automation where messages arrive rapidly, contain semi-structured information, and need to be converted into reliable machine-readable events.

This repository is the **public, sanitized implementation of that engineering pattern**. It contains synthetic signal data and a paper-only execution adapter. It does **not** connect to a live trading account, brokerage, Telegram channel, or MetaTrader 5 terminal.

### Engineering capabilities

- Async message accumulation
- Semi-structured text parsing
- Typed events with **Pydantic**
- Optional **Anthropic Claude API** extraction
- Explicit validation of required fields
- Paper/simulation execution boundary
- Unit tests and GitHub Actions CI

## Architecture

~~~text
Message fragments
      |
      v
MessageAccumulator
      |
      v
Signal parser
      |
      v
Pydantic TradeSignal
      |
      +----> optional Claude extraction
      |
      v
PaperExecutor
      |
      v
SimulatedOrder
~~~

See docs/architecture.md for the design notes.

## Repository structure

~~~text
telegram-mt5-trading-bot/
├── .github/workflows/ci.yml
├── docs/architecture.md
├── sample_data/signal.txt
├── src/
│   ├── __init__.py
│   ├── accumulator.py
│   ├── executor.py
│   ├── main.py
│   ├── models.py
│   └── signal_parser.py
├── tests/test_signal.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
~~~

## Quick start

~~~bash
git clone https://github.com/pranay-eligeti/telegram-mt5-trading-bot.git
cd telegram-mt5-trading-bot
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
~~~

### Run the synthetic demo

~~~bash
python -m src.main --input sample_data/signal.txt
~~~

The command parses the synthetic message fragments and prints a **SimulatedOrder**. No live order is created.

### Run tests

~~~bash
pytest -q
~~~

## Example event

The fixture represents a synthetic signal containing an instrument, direction, entry, stop-loss, and take-profit levels. The parser converts those fragments into a typed `TradeSignal` object before the paper executor produces a simulated order.

## LLM extraction

`parse_with_claude(...)` is an optional provider for less-structured messages. Configure `ANTHROPIC_API_KEY` locally; CI never calls the external model.

The LLM prompt explicitly asks the model to use `null` for missing values and never invent prices.

## Safety boundary

The public implementation intentionally stops at a **paper/simulation layer**. It contains no broker credentials, live execution code, private channel identifiers, or automated order placement.

For financial software, any live deployment requires separate risk controls, authorization, testing, monitoring, and compliance review. This repository is a software-engineering demonstration, not trading advice or a recommendation to use a particular strategy.

## Privacy and security

Never commit Telegram session files, API credentials, broker credentials, account identifiers, private messages, or private trading-channel content.

## Portfolio note

The value of this project is the engineering pipeline: **event ingestion → normalization → typed state → optional AI extraction → controlled action boundary**.

## Author

**Pranay Eligeti**

[LinkedIn](https://www.linkedin.com/in/pranay-eligeti) · [GitHub](https://github.com/pranay-eligeti)
