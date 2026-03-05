## Why

The bot currently only collects timed bonuses but doesn't spend accumulated coins. This change automates crate purchases whenever the wallet has enough coins, maximizing the value of the earned in-game currency.

## What Changes

- New GitHub Actions workflow (`buy_crate.yml`) that runs every 10 minutes
- Workflow checks `client.account().wallet["coins"]` before each purchase attempt
- If coins >= 1000, calls `client.buy_crate()` and loops; if coins < 1000, the workflow exits (stops further scheduling until the next manual trigger or coin accumulation cycle)
- New Python script (`buy_crate.py`) that encapsulates the coin-check + buy logic

## Capabilities

### New Capabilities
- `buy-crate`: Checks wallet coin balance and purchases a crate when balance meets the threshold (>= 1000 coins); exits cleanly when balance drops below threshold.

### Modified Capabilities
<!-- No existing capability requirements are changing. -->

## Impact

- New file: `buy_crate.py` — script run by the workflow
- New file: `.github/workflows/buy_crate.yml` — scheduled workflow (every 10 minutes)
- Uses same `EMAIL` / `PASSWORD` secrets as the existing workflow
- Depends on `rbrapi` methods: `client.account()`, `client.buy_crate()`
- No changes to `main.py`, `logger.py`, or the existing bonus-collection workflow
