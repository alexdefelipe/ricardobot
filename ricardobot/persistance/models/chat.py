import peewee as pw

from ricardobot.persistance.models import BaseModel


class Chat(BaseModel):
    chat_id = pw.CharField(unique=True)
