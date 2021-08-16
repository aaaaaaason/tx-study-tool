"""Entrypoint for this tool."""
import argparse
import logging as log
import os
import sys
import signal
from typing import List

from txtool import (
    case,
    config,
    database,
    logging,
    runner,
)


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse arguments from input.

    Args:
      args: Expect to be sys.argv[1:].
    Returns:
      Parsed result.
    """
    parser = argparse.ArgumentParser('Transaction Study Tool')

    parser.add_argument('-e',
                        '--env',
                        type=str,
                        default='.env',
                        dest='env',
                        help='The file path to load environment variables.')

    parser.add_argument('case',
                        metavar='case',
                        type=str,
                        help='The file path to load target test case.')

    return parser.parse_args(args)


def main():
    """Entrypoint is here."""
    args = parse_args(sys.argv[1:])

    conf = config.setup(args.env)

    logging.setup(conf.logging_level)

    reader = case.Reader(args.case)

    engine = database.create_engine(conf, reader.get_engine())

    def handler(signum, _):
        log.info('Receive signal %s, start running teardown.',\
             signal.Signals(signum).name)
        engine.close()

    signal.signal(signal.SIGINT, handler)

    runner.Runner(conf).run(reader, engine)
