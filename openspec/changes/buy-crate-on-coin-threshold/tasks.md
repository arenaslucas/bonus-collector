## 1. Buy-Crate Script

- [x] 1.1 Create `buy_crate.py` with argument parsing (`--email`, `--password`, `--no-logging`) and env-var override (`EMAIL`, `PASSWORD`)
- [x] 1.2 Authenticate with `RocketBotRoyale(email, password)` and fetch coin balance via `client.account().wallet["coins"]`
- [x] 1.3 Exit with code 0 and log insufficient-balance message when coins < 1000
- [x] 1.4 Call `client.buy_crate()` when coins >= 1000 and log success
- [x] 1.5 Catch `LootBoxError` (and other relevant errors from `rbrapi.errors`) and exit with non-zero code on failure

## 2. GitHub Actions Workflow

- [x] 2.1 Create `.github/workflows/buy_crate.yml` with `schedule: "*/10 * * * *"` and `workflow_dispatch` triggers
- [x] 2.2 Configure workflow to use Python 3.11, install dependencies from `requirements.txt`, and run `buy_crate.py` with `EMAIL` and `PASSWORD` secrets
