from ricardobot.persistance.models import Order, User, Chat, Version


class RecreateDb:
    @staticmethod
    def run():
        try:
            for model in (Order, User, Chat):
                model.drop_table()
                model.create_table()
            Version.create_table()
        except Exception:
            print("Ha ocurrido un error durante la reinicilización de la base de datos")
