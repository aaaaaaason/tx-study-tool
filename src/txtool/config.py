"""Configuration store is here"""
import os
import logging
import dotenv

_config = None


class EnvironmentVariableNotFoundError(Exception):
    pass


def _must_read_env(name: str, default: str = None) -> str:
    """Read environment variable.

    The program raises EnvironmentVariableNotFoundError if
    target name does not exists, and default value is not specified.

    Args:
      name: The name of the environment variable.
      default: Default value when no such variable.
    Returns:
      The value of the environment varible.
    Raises:
      EnvironmentVariableNotFoundError: If
    """
    value = os.getenv(name, default)
    if not value:
        logging.fatal(
            "Cannot read variable \"%s\" "
            "and no default value specifed.", name)
        raise EnvironmentVariableNotFoundError("No")
    return value


class Config:
    """Stores configuration for properly initialize other module."""
    def __init__(self, envfile: str):
        """Initialize config object.

        Args:
          envfile: Filepath to read dotenv.
        """
        logging.info("Initializing config object.")
        if os.path.exists(envfile):
            logging.info("Loading dotenv from path \"%s\"", envfile)
            dotenv.load_dotenv(envfile)

        # Postgres
        self.postgres_user = _must_read_env("POSTGRES_USER")
        self.postgres_passwd = _must_read_env("POSTGRES_PASSWD")
        self.postgres_host = _must_read_env("POSTGRES_HOST")
        self.postgres_port = _must_read_env("POSTGRES_PORT")
        self.postgres_db = _must_read_env("POSTGRES_DB")

        # MySQL
        self.mysql_user = _must_read_env("MYSQL_USER")
        self.mysql_passwd = _must_read_env("MYSQL_PASSWD")
        self.mysql_host = _must_read_env("MYSQL_HOST")
        self.mysql_port = _must_read_env("MYSQL_PORT")
        self.mysql_db = _must_read_env("MYSQL_DB")

        # App
        self.logging_level = _must_read_env("APP_LOGGING_LEVEL", "INFO")


def setup(envfile: str = ".env") -> Config:
    """Returns a singleton Config object

    Args:
      envfile: Filepath to read dotenv.
    Returns:
      Config object for quering configuration.
    """
    global _config
    if not _config:
        _config = Config(envfile)
    return _config
