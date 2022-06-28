import os
from enum import Enum

from playhouse.pool import PooledSqliteDatabase, PooledMySQLDatabase, PooledPostgresqlDatabase

from ricardobot.exceptions.database_parameter_missing_exception import DatabaseParameterMissingException


class DatabaseProvider(Enum):
    SQLITE = 1
    MYSQL = 2
    POSTGRESQL = 3


class DatabaseConfigurator:

    @staticmethod
    def get_connection(provider: DatabaseProvider):
        if provider is DatabaseProvider.SQLITE:
            return PooledSqliteDatabase(DatabaseConfigurator.get_configuration_parameters())
        else:
            db_name, db_user, db_pass, db_host, db_port = DatabaseConfigurator.get_configuration_parameters()
            if provider is DatabaseProvider.MYSQL:
                return PooledMySQLDatabase(db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

            if provider is DatabaseProvider.MYSQL:
                return PooledPostgresqlDatabase(db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

    @staticmethod
    def get_configuration_parameters():
        db_path = f"{os.environ['RICARDOBOT_ROOT_PATH']}/{os.getenv('DB_PATH', None)}"
        if db_path is not None:
            return db_path
        return tuple(DatabaseConfigurator.get_database_parameter(param) for param in ("db_name", "db_user", "db_pass",
                                                                                      "db_host", "db_port"))

    @staticmethod
    def get_database_parameter(param: str):
        param_value = os.getenv(param.upper(), None)
        if param_value is None:
            raise DatabaseParameterMissingException(param)
