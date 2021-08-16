"""Test database api."""
import pytest
from txtool import (
    database,
    step,
)

from tests import (
    stub,
    spy,
)


@pytest.mark.small
def test_create_engine_postgres():
    for database_name in ('POSTGRES', 'POSTGRESQL', 'PG'):
        # When I start create engine.
        engine = database.create_engine(stub.Config(), database_name)
        # Then I should get corresponding engine.
        assert isinstance(engine, database.PostgresEngine),\
            f'Expect to get postgres engine but got {type(engine)}.'


@pytest.mark.small
def test_create_engine_mysql():
    for database_name in ('MYSQL', 'MySQL'):
        # When I start create engine.
        engine = database.create_engine(stub.Config(), database_name)
        # Then I should get corresponding engine.
        assert isinstance(engine, database.MySQLEngine),\
            f'Expect to get mysql engine but got {type(engine)}.'


@pytest.mark.small
def test_engine_execute_step():
    # Given I create a spy engine and a step.
    engine = spy.Engine()
    each = step.Step(0, 'SELECT * FROM item;')

    # When I run the step.
    engine.execute(each)

    # Then I should have a connection object.
    # pylint: disable=protected-access
    session = engine._sessions.get(0)
    assert session, ('Expect to have a session with id 0, but got nothing.')

    # And this connection object should execute this statement.
    last_stmt = session.last_stmt
    assert last_stmt == 'SELECT * FROM item;', (
        f'Got unexpected last statement "{last_stmt}"')
