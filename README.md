# 📈 Telegram-to-MetaTrader5 Trading Bot

> An automated trading bot that listens to a Telegram prop trading channel, parses mixed Hindi/English signals using the Anthropic Claude API, and executes trades directly on MetaTrader5 — fully hands-free.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude%20API-blueviolet)
![MetaTrader5](https://img.shields.io/badge/MetaTrader5-Trading-green)
![Telethon](https://img.shields.io/badge/Telethon-Telegram%20API-blue)

---

## What It Does

Monitors a private Telegram trading channel for BTC/USDT and Gold signals (sent in a mix of Hindi and English), intelligently parses them using Claude API, and automatically places trades on a MetaTrader5 prop account — targeting TP3 (the furthest take profit) for maximum gain per trade.

---

## The Problem It Solves

Prop trading signal channels send signals rapidly, often in bursts of multiple messages, in informal mixed-language text. Manual execution is too slow and error-prone. This bot:

- Catches every signal instantly
- Handles message bursts (batching via `MessageAccumulator`)
- Understands informal Hindi/English mixed text
- Executes trades in milliseconds

---

## How It Works

```
Telegram Channel (Hindi/English signals)
        │
        ▼
Telethon listener (real-time message capture)
        │
        ▼
MessageAccumulator (batches rapid-fire messages, 2s window)
        │
        ▼
Anthropic Claude API
  Prompt: "Extract trade parameters from this signal text"
  Output: {
    instrument: "GOLD",
    direction: "BUY",
    entry: 2345.50,
    tp1: 2350.00,
    tp2: 2355.00,
    tp3: 2362.00,   ← bot targets this
    sl: 2338.00
  }
        │
        ▼
MetaTrader5 Python Library
  → Places order at entry price
  → Sets SL and TP3
  → Confirms execution
        │
        ▼
Trade Active on FundedFirm Prop Account
```

---

## Tech Stack

| Tool                       | Purpose                            |
| -------------------------- | ---------------------------------- |
| Python 3.10+               | Core bot logic                     |
| Telethon                   | Telegram MTProto API client        |
| Anthropic Claude API       | Signal parsing (Hindi/English NLP) |
| MetaTrader5 Python library | Trade execution                    |
| asyncio                    | Async message handling             |
| MessageAccumulator         | Custom class for burst batching    |

---

## Key Design Decisions

**Why Claude API for parsing?**
Signal text is informal, multilingual, and inconsistent. Regex fails on varied formats. Claude reliably extracts structured trade data from any phrasing.

**Why target only TP3?**
TP3 is the furthest take profit — maximizes gain per trade on a prop account where drawdown limits matter more than win rate.

**Why MessageAccumulator?**
Signal channels often send a trade in 3-5 rapid messages (entry in one, TPs in another, SL in another). The accumulator batches all messages within a 2-second window before sending to Claude, ensuring complete signal context.

---

## Project Structure

```
telegram-mt5-trading-bot/
├── src/
│   ├── bot.py                  # Main entry point
│   ├── accumulator.py          # MessageAccumulator class
│   ├── signal_parser.py        # Claude API integration
│   ├── trader.py               # MT5 order execution
│   └── utils.py                # Logging, helpers
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/pranay-eligeti/telegram-mt5-trading-bot.git
cd telegram-mt5-trading-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Fill in all credentials
```

### 4. Run the bot

```bash
python src/bot.py
```

---

## Environment Variables

```env
# .env.example

# Telegram API (get from my.telegram.org)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_CHANNEL_ID=your_channel_id

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key

# MetaTrader5
MT5_LOGIN=your_mt5_account_number
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_broker_server

# Bot config
ACCUMULATOR_WINDOW_SECONDS=2
TARGET_TP=3
```

---

## Requirements

```
telethon>=1.34.0
anthropic>=0.25.0
MetaTrader5>=5.0.45
python-dotenv>=1.0.0
```

> ⚠️ **Note:** MetaTrader5 Python library only works on Windows.

---

## Disclaimer

This bot is for educational and personal use only. Trading involves significant financial risk. Never use this on a live funded account without thorough testing. The author is not responsible for any financial losses.

---

## Author

**Pranay Eligeti** — [linkedin.com/in/pranay-eligeti](https://linkedin.com/in/pranay-eligeti)
