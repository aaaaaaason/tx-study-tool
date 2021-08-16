"""Test case runner functions."""
import pytest
from txtool import (
    case,
    runner,
)

from tests import (
    stub,
    spy,
)


@pytest.mark.medium
def test_runner_run():
    # Given I create a case reader.
    case_reader = case.Reader('src/tests/data/basic_case.yaml')
    config = stub.Config()
    engine = spy.Engine()

    # When I start runner.
    r = runner.Runner(config)

    # Then everything should be okay.
    r.run(case_reader, engine)
