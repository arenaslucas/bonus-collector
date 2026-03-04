# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RocketBotRoyale Bonus Collector — a Python automation tool that collects timed bonuses from the RocketBotRoyale game via its unofficial API (`rbrapi`). Designed for scheduled execution via GitHub Actions.

## Installation

```bash
pip install rbr-api-fork
```

## Running

```bash
# With CLI args
python main.py --email "your_email" --password "your_password"

# With environment variables (preferred for CI/CD)
EMAIL="your_email" PASSWORD="your_password" python main.py

# Suppress logging output
python main.py --email "your_email" --password "your_password" --no-logging
```

## Architecture

The project is intentionally minimal:

- [main.py](main.py) — Entry point. Parses args/env vars, authenticates with `RocketBotRoyale(email, password)`, calls `client.collect_timed_bonus()`, and handles `AuthenticationError`, `CollectTimedBonusError`, and `LootBoxError` from `rbrapi.errors`.
- [logger.py](logger.py) — Thin wrapper around Python's `logging` module. Pass `Logger(__name__)` or `None` to disable logging.

## CI/CD

The GitHub Actions workflow ([.github/workflows/run_main.yml](.github/workflows/run_main.yml)) runs every 34 minutes on a cron schedule and on manual dispatch. It uses `EMAIL` and `PASSWORD` GitHub repository secrets. Python version is pinned to **3.11**.

## Credentials

- CLI: `--email` / `--password`
- Environment: `EMAIL` / `PASSWORD` (takes precedence over CLI args)
- For GitHub Actions: configure as repository secrets named `EMAIL` and `PASSWORD`
