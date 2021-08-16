"""Test case reader."""
import pytest
from txtool import (
    case,
)

@pytest.mark.medium
def test_case_reader():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/basic_case.yaml'

    # When I create a new case reader.
    reader = case.Reader(run_case)

    # Then I should get proper output.
    engine = reader.get_engine()
    assert engine == 'postgres', (
        f'Expect to get "postgres", but got "{engine}"')

    # Check setup:
    setup_steps = reader.get_steps_for_setup()
    assert len(setup_steps) == 1,\
        f'Expect setup steps is a list with len 1, got {len(setup_steps)}'

    step = setup_steps[0]
    assert step.session_id == -1, (
        'Expect to use connection id -1 for every test setup step, '
        f'but got {step.session_id}.')

    assert step.statement == (
        'CREATE TABLE IF NOT EXISTS item (id INT PRIMARY KEY);'),\
        'Got unexpected setup step.'

    # Check teardown:
    teardown_steps = reader.get_steps_for_teardown()
    assert len(teardown_steps) == 1,\
        f'Expect teardown steps is a list with len 1, got {len(teardown_steps)}'

    step = teardown_steps[0]
    assert step.session_id == -1, (
        'Expect to use connection id -1 for every test teardown step, '
        f'but got {step.session_id}.')

    assert step.statement == 'DROP TABLE IF EXISTS item;',\
        'Got unexpected teardown step.'

    # Check steps:
    steps = reader.get_steps()
    assert len(steps) == 2,\
        f'Expect steps is a list with len 2, got {len(steps)}'

    step = steps[0]
    assert step.session_id == 1, (
        f'Expect to get connection id 1 but got {step.session_id}.')

    assert step.statement == (
        "INSERT INTO item (id, name, count) VALUES (1, 'book', 5);"),\
        'Got unexpected step.'

    step = steps[1]
    assert step.session_id == 0, (
        f'Expect to get connection id 0 but got {step.session_id}.')

    assert step.statement == 'SELECT * FROM item;',\
        'Got unexpected step.'


@pytest.mark.medium
def test_case_reader_case_not_found():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/not_found_case.yaml'

    # Then I should get exception.
    with pytest.raises(case.CaseNotFoundError):
        # When I create a new case reader.
        case.Reader(run_case)


@pytest.mark.medium
def test_case_reader_engine_not_found():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/no_engine_case.yaml'

    # Then I should get exception.
    with pytest.raises(case.EngineNotFoundError):
        # When I create a new case reader.
        case.Reader(run_case).get_engine()


@pytest.mark.medium
def test_case_reader_setup_not_found():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/no_setup_case.yaml'

    # Then I should get exception.
    with pytest.raises(case.SetupStepsNotFoundError):
        # When I create a new case reader.
        case.Reader(run_case).get_steps_for_setup()


@pytest.mark.medium
def test_case_reader_teardown_not_found():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/no_teardown_case.yaml'

    # Then I should get exception.
    with pytest.raises(case.TeardownStepsNotFoundError):
        # When I create a new case reader.
        case.Reader(run_case).get_steps_for_teardown()


@pytest.mark.medium
def test_case_reader_steps_not_found():
    # Given I choose a valid case and a config object.
    run_case = 'src/tests/data/no_step_case.yaml'

    # Then I should get exception.
    with pytest.raises(case.StepsNotFoundError):
        # When I create a new case reader.
        case.Reader(run_case).get_steps()
