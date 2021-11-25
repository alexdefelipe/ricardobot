from ricardobot.persistance.utils.database_config import DatabaseConfigurator, DatabaseProvider

db = DatabaseConfigurator.get_connection(DatabaseProvider.SQLITE)
