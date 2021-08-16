"""Define case runner."""
import logging
from txtool import (
    config,
    case,
    database,
)


class Runner:
    """Read and run the test case."""
    def __init__(self, conf: config.Config):
        self.conf = conf

    def run(self, reader: case.Reader, engine: database.Engine):
        logging.info('Start running setup.')
        for step in reader.get_steps_for_setup():
            engine.execute(step)

        logging.info('Start running steps.')
        try:
            for step in reader.get_steps():
                engine.execute(step, mask_exception=True)
        # pylint: disable=broad-except
        except Exception as e:
            logging.error('Got exception "%s" in steps.', e)

        logging.info('Start running teardown.')
        for step in reader.get_steps_for_teardown():
            engine.execute(step)

        logging.info('Done.')
