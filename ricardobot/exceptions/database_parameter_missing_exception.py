class DatabaseParameterMissingException(Exception):
    def __init__(self, db_param):
        self.db_param = db_param

    def __str__(self):
        return f'Error when establishing a database connection. Either db_path or {self.db_param} are missing'
