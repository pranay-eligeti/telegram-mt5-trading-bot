# Architecture

This repository is a sanitized portfolio implementation of an event-driven signal-ingestion and structured-parsing workflow.

## Flow

~~~text
Message fragments
      |
      v
MessageAccumulator
      |
      v
Structured parser
      |
      v
Pydantic TradeSignal
      |
      +--> optional Claude extraction provider
      |
      v
PaperExecutor
      |
      v
SimulatedOrder
~~~

## Engineering decisions

- Message accumulation is separated from parsing so bursty inputs can be normalized before interpretation.
- The normalized event is typed with Pydantic.
- LLM extraction is optional; deterministic parsing keeps tests reproducible.
- The public repository includes a paper executor only. It does not connect to MetaTrader 5 or a live brokerage account.
- Credentials and private channel identifiers are never stored in source control.
- Synthetic fixtures are used for CI.
