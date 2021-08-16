"""Provide database utility."""
import logging
from typing import (
    Any,
    Callable,
    Dict,
)
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.exc import (
    IntegrityError,
    ResourceClosedError,
)

from txtool import (
    config,
    step,
)


def get_default_session_id() -> int:
    """Returns seesion id for setup and teardown"""
    return -1


class SessionMaker:
    """An interface to generate"""


class Engine:
    """Base class of database engine for typing annotation"""
    def __init__(self, session_maker: Callable):
        self._sessions: Dict[int, Any] = dict()
        self._session_maker = session_maker

    def execute(self, each: step.Step, mask_exception: bool = False):
        if each.session_id not in self._sessions:
            self._sessions[each.session_id] = self._session_maker()
        session = self._sessions[each.session_id]

        results = None
        try:
            results = session.execute(each.statement)
        except ResourceClosedError:
            logging.info('Got resource closed error')
        except IntegrityError as e:
            if not mask_exception:
                raise
            logging.info('Got Exception "%s"', type(e))

        stmt = each.statement if len(each.statement) <= 60 \
            else each.statement[:60] + '...'

        logging.info('Session ID [%d]: %s', each.session_id, stmt)

        # TODO: Really bad hack.
        if each.statement.strip().startswith('SELECT') and results:
            for result in results:
                logging.info('Session ID [%d]: %s', each.session_id, result)

    def close(self):
        default_session_id = get_default_session_id()
        for session_id, session in self._sessions.items():
            if session_id == default_session_id:
                continue
            session.close()


class PostgresEngine(Engine):
    """Engine to run database query against PostgreSQL."""
    def __init__(self, conf: config.Config):
        self._url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            conf.postgres_user,
            conf.postgres_passwd,
            conf.postgres_host,
            conf.postgres_port,
            conf.postgres_db,
        )
        session_maker = orm.sessionmaker(
            #autocommit=True,
            bind=sa.create_engine(self._url, ))
        super().__init__(session_maker)


class MySQLEngine(Engine):
    """Engine to run database query against MySQL."""
    def __init__(self, conf: config.Config):
        self._url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            conf.mysql_user,
            conf.mysql_passwd,
            conf.mysql_host,
            conf.mysql_port,
            conf.mysql_db,
        )
        session_maker = orm.sessionmaker(
            #autocommit=True,
            bind=sa.create_engine(self._url, ))
        super().__init__(session_maker)


class UnsupportedDatabaseError(Exception):
    pass


def create_engine(conf: config.Config, database_name: str) -> Engine:
    """Create an Engine object.

    Args:
      database_name: Like postgres, mysql, case insensitive.
    """
    name = database_name.lower()
    if name in ('postgres', 'postgresql', 'pg'):
        return PostgresEngine(conf)
    elif name == 'mysql':
        return MySQLEngine(conf)
    raise UnsupportedDatabaseError(
        f'Got database name {database_name} which is not supported.')
