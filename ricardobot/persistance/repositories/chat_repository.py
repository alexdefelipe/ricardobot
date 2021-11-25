import peewee as pw

from ricardobot.exceptions.resource_already_exists_exception import ResourceAlreadyExistsException
from ricardobot.persistance.models import Chat


class ChatRepository:
    @staticmethod
    def get(chat_id: int):
        return Chat.get(Chat.chat_id == chat_id)

    @staticmethod
    def create(chat_id: int):
        try:
            chat = Chat.create(chat_id=chat_id)
            return chat
        except pw.IntegrityError:
            raise ResourceAlreadyExistsException("Chat", chat_id)

    @staticmethod
    def get_all():
        return Chat.select()
