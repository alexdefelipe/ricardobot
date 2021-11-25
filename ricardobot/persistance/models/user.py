import peewee as pw

from ricardobot.persistance.models import BaseModel, Chat


class User(BaseModel):
    user_id = pw.BigIntegerField(unique=True)
    chat = pw.ForeignKeyField(Chat, Chat.chat_id)
    name = pw.CharField()
