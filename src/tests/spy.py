"""Define spies."""
from txtool import (
    database, )


class Session:
    """Spy session for test."""
    def __init__(self):
        self.last_stmt = None

    def execute(self, stmt: str):
        self.last_stmt = stmt
        return None

class SessionMaker:
    """Return a spy session."""
    def __call__(self):
        return Session()


class Engine(database.Engine):
    """Test engine, no connection inside."""
    def __init__(self):
        super().__init__(SessionMaker())
