"""Define stubs."""


class Config:
    """For test only."""
    def __init__(self):
        # Postgres
        self.postgres_user = 'user'
        self.postgres_passwd = 'pass'
        self.postgres_host = 'localhost'
        self.postgres_port = '5432'
        self.postgres_db = 'database'

        # MySQL
        self.mysql_user = 'user'
        self.mysql_passwd = 'pass'
        self.mysql_host = 'localhost'
        self.mysql_port = '3306'
        self.mysql_db = 'database'
