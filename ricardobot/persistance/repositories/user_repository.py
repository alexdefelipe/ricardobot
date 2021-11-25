from typing import List

import peewee as pw

from telebotify.models.user import User as BotUser
from ricardobot.exceptions.resource_already_exists_exception import ResourceAlreadyExistsException
from ricardobot.exceptions.resource_not_found_exception import ResourceNotFoundException
from ricardobot.persistance.models import User, Chat


class UserRepository:
    @staticmethod
    def get(user_id: int) -> User:
        try:
            return User.get(User.user_id == user_id)
        except pw.DoesNotExist:
            raise ResourceNotFoundException("User", user_id)

    @classmethod
    def get_or_create(cls, user: BotUser, chat: Chat) -> User:
        name = user.username if user.username is not None else user.first_name
        user, _ = User.get_or_create(user_id=user.user_id, chat=chat, name=name)
        return user

    @staticmethod
    def get_all() -> List[User]:
        users = User.select()
        return users

    @staticmethod
    def create(user_id: int) -> User:
        try:
            return User.create(user_id=user_id)
        except pw.IntegrityError:
            raise ResourceAlreadyExistsException("User", user_id)
