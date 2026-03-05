## Context

The project currently runs a single GitHub Actions workflow (`run_main.yml`) on a 34-minute cron to collect timed bonuses. Coins accumulate in the wallet but are never spent. The unofficial `rbrapi` library exposes `client.account().wallet["coins"]` and `client.buy_crate()`, which are sufficient to implement automated spending.

The workflow must self-terminate when coins drop below 1000 to avoid failed purchase attempts and unnecessary API calls.

## Goals / Non-Goals

**Goals:**
- Add a dedicated Python script (`buy_crate.py`) that checks coin balance and buys one crate per run
- Add a new GitHub Actions workflow scheduled every 10 minutes
- The workflow exits with a success code when coins < 1000 (soft stop — no retry until the next scheduled run)

**Non-Goals:**
- Modifying the existing bonus-collection workflow or `main.py`
- Handling multiple crate types or configurable thresholds (hardcoded 1000 for now)
- Persisting purchase history or sending notifications

## Decisions

**Single-purchase-per-run vs. loop-until-broke**
The workflow runs every 10 minutes via cron. Each invocation buys at most one crate and exits. This avoids runaway loops inside a single job and keeps logs clean per GitHub Actions run. The cron schedule provides the repetition.

Alternative considered: loop inside `buy_crate.py` buying crates until coins < 1000. Rejected because it risks hitting API rate limits in a single run and makes the GitHub Actions log harder to read.

**Exit strategy: success exit vs. failure exit when coins < 1000**
Exiting with code 0 when coins < 1000 (treated as "nothing to do") avoids false-positive workflow failures in the GitHub Actions UI. A non-zero exit would mark the run as failed, which is misleading.

**Script structure: follow `main.py` conventions**
`buy_crate.py` mirrors `main.py`'s argument/env-var pattern (`--email`, `--password`, `--no-logging`) and uses the same `Logger` wrapper so the codebase stays consistent.

## Risks / Trade-offs

- [API rate limiting] Buying a crate every 10 minutes could trigger rate limits → Mitigation: single purchase per run; if `buy_crate()` raises an error, log and exit non-zero so the GitHub Actions UI flags it.
- [Coin drain] Automation may deplete coins faster than intended → Mitigation: the 1000-coin threshold is a guard; acceptable by design.
- [Cron overlap] GitHub Actions cron is not guaranteed to fire exactly every 10 minutes under load → Mitigation: each run is idempotent (check-then-buy); overlapping runs are safe.
