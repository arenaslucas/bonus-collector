import argparse
import os
import sys
from rbrapi import RocketBotRoyale
from rbrapi.errors import AuthenticationError, LootBoxError
from logger import Logger

COIN_THRESHOLD = 1000


def parse_args():
    parser = argparse.ArgumentParser(description="RocketBotRoyale crate buyer.")
    parser.add_argument("--email", type=str, help="Email for RocketBotRoyale account")
    parser.add_argument("--password", type=str, help="Password for RocketBotRoyale account")
    parser.add_argument("--no-logging", action="store_true", help="Disable logging")
    return parser.parse_args()


def main():
    args = parse_args()

    email = os.getenv("EMAIL") or args.email
    password = os.getenv("PASSWORD") or args.password

    if not email or not password:
        print("Missing credentials: please set EMAIL and PASSWORD environment variables.")
        sys.exit(1)

    logger = None if args.no_logging else Logger(__name__)

    try:
        client = RocketBotRoyale(email, password)

        coins = client.account().wallet["coins"]
        if logger:
            logger.info(f"Current coin balance: {coins}.")

        if coins < COIN_THRESHOLD:
            if logger:
                logger.info(f"Insufficient coins ({coins} < {COIN_THRESHOLD}). Nothing to buy.")
            sys.exit(0)

        award = client.buy_crate()
        if logger:
            logger.info(f"Crate purchased successfully. Award: {award.award_id}")

    except AuthenticationError as e:
        if logger:
            logger.error(f"Unable to authenticate: {e}")
        sys.exit(1)
    except LootBoxError as e:
        if logger:
            logger.error(f"Unable to buy crate: {e}")
        sys.exit(1)
    except Exception as e:
        if logger:
            logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
