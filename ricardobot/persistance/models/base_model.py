import peewee as pw

from ricardobot.persistance import db


class BaseModel(pw.Model):
    class Meta:
        database = db
