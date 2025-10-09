import argparse
import os
from rbrapi import RocketBotRoyale
from rbrapi.errors import AuthenticationError, CollectTimedBonusError, LootBoxError
from logger import Logger


def parse_args():
    parser = argparse.ArgumentParser(description="RocketBotRoyale bonus collector.")
    parser.add_argument("--email", type=str, help="Email for RocketBotRoyale account")
    parser.add_argument("--password", type=str, help="Password for RocketBotRoyale account")
    parser.add_argument("--no-logging", action="store_true", help="Disable logging")
    parser.add_argument("--auto-open-crates", action="store_true", help="Automatically open crates if available")
    return parser.parse_args()


def main():
    args = parse_args()

    # Prefer environment variables for secrets in CI/CD
    email = args.email or os.getenv("EMAIL")
    password = args.password or os.getenv("PASSWORD")

    if not email or not password:
        print("❌ Missing credentials: please set EMAIL and PASSWORD environment variables.")
        return

    logger = None if args.no_logging else Logger(__name__)

    try:
        client = RocketBotRoyale(email, password)

        client.collect_timed_bonus()
        if logger:
            logger.info("✅ Coins collected successfully.")

        coins = client.account().wallet["coins"]
        if logger:
            logger.info(f"💰 Your coins now: {coins}.")

        if args.auto_open_crates and coins >= 1000:
            award = client.buy_crate()
            if logger:
                logger.info(f"🎁 Crate award: {award.award_id}")

    except AuthenticationError as e:
        if logger:
            logger.error(f"Unable to authenticate: {e}")
    except CollectTimedBonusError as e:
        if logger:
            logger.info(f"Bonus not available yet: {e}")
    except LootBoxError as e:
        if logger:
            logger.error(f"Unable to open crates: {e}")
    except Exception as e:
        if logger:
            logger.exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
