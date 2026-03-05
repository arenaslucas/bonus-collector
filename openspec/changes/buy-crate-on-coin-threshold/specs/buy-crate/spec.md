## ADDED Requirements

### Requirement: Coin balance check before purchase
The system SHALL read the authenticated user's wallet coin balance via `client.account().wallet["coins"]` before attempting any crate purchase.

#### Scenario: Balance at or above threshold
- **WHEN** `client.account().wallet["coins"]` returns a value >= 1000
- **THEN** the script SHALL proceed to call `client.buy_crate()`

#### Scenario: Balance below threshold
- **WHEN** `client.account().wallet["coins"]` returns a value < 1000
- **THEN** the script SHALL log that the balance is insufficient and exit with code 0 (no purchase attempted)

### Requirement: Crate purchase execution
The system SHALL call `client.buy_crate()` when the coin balance meets the threshold.

#### Scenario: Successful purchase
- **WHEN** `client.buy_crate()` completes without raising an exception
- **THEN** the script SHALL log a success message (including remaining coin balance if available) and exit with code 0

#### Scenario: Purchase failure
- **WHEN** `client.buy_crate()` raises an exception (e.g., `LootBoxError`)
- **THEN** the script SHALL log the error and exit with a non-zero code

### Requirement: Scheduled GitHub Actions workflow
The system SHALL provide a GitHub Actions workflow that runs the buy-crate script on a schedule.

#### Scenario: Workflow triggers every 10 minutes
- **WHEN** the cron schedule fires (`*/10 * * * *`)
- **THEN** the workflow SHALL authenticate and run `buy_crate.py` using `EMAIL` and `PASSWORD` secrets

#### Scenario: Manual workflow dispatch
- **WHEN** a user triggers the workflow manually via `workflow_dispatch`
- **THEN** the workflow SHALL behave identically to a scheduled run

### Requirement: CLI and environment variable credential support
The script SHALL accept credentials via `--email`/`--password` CLI arguments or `EMAIL`/`PASSWORD` environment variables, with environment variables taking precedence.

#### Scenario: Environment variables provided
- **WHEN** `EMAIL` and `PASSWORD` environment variables are set
- **THEN** the script SHALL use them, ignoring any CLI arguments

#### Scenario: CLI arguments provided without env vars
- **WHEN** `--email` and `--password` flags are passed and no environment variables are set
- **THEN** the script SHALL use the CLI argument values
