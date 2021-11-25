from typing import List

from telebotify.models.message import Message
from ricardobot.exceptions.resource_not_found_exception import ResourceNotFoundException
from ricardobot.persistance.models import Chat, User, Order
from ricardobot.persistance.models.order import OrderStatus
from ricardobot.persistance.repositories.chat_repository import ChatRepository
from ricardobot.persistance.repositories.order_repository import OrderRepository
from ricardobot.persistance.repositories.user_repository import UserRepository
from ricardobot.utils.date_utils import DateUtils


class OrderService:
    @staticmethod
    def get_order(user: User, chat: Chat) -> Order:
        where_clauses = [
            Order.chat == chat,
            Order.user == user,
            Order.date >= DateUtils.get_last_friday()
        ]
        order = OrderRepository.find_one(where_clauses)
        return order[0]

    @staticmethod
    def get_confirmed_order(user: User, chat: Chat) -> Order:
        where_clauses = [
            Order.chat == chat,
            Order.user == user,
            Order.status == OrderStatus.NOT_CONFIRMED,
            Order.date >= DateUtils.get_last_friday()
        ]
        order = OrderRepository.find_one(where_clauses)
        return order[0]

    @staticmethod
    def get_current_week_orders(message):
        chat = ChatRepository.get(message.chat.chat_id)
        where_clauses = [
            Order.chat == chat,
            Order.status == OrderStatus.CONFIRMED,
            Order.date >= DateUtils.get_last_friday()
        ]
        return OrderRepository.find(where_clauses)

    @staticmethod
    def create(chat: Chat, user: User, first_part: str, second_part: str, drink: str) -> Order:
        order = Order(chat=chat, user=user, first_part=first_part, second_part=second_part, drink=drink)
        new_order_id = OrderRepository.create(order)
        return OrderRepository.get(new_order_id)

    @staticmethod
    def start_order(message: Message, params: List[str]) -> Order:
        chat = ChatRepository.get(message.chat.chat_id)
        user = UserRepository.get_or_create(message.from_user, chat)
        return OrderService.create(chat, user, *params)

    @classmethod
    def confirm_order(cls, message) -> None:
        try:
            chat = ChatRepository.get(message.chat.chat_id)
            user = UserRepository.get(message.from_user.user_id)

            update_clauses = {'status': OrderStatus.CONFIRMED}
            where_clauses = [
                Order.chat == chat,
                Order.user == user,
                Order.status == OrderStatus.NOT_CONFIRMED,
                Order.date.between(DateUtils.get_last_friday(), DateUtils.get_next_friday())
            ]

            OrderRepository.update(update_clauses, where_clauses)
        except ResourceNotFoundException as ex:
            raise ex

    @classmethod
    def cancel_order(cls, message) -> None:
        try:
            chat = ChatRepository.get(message.chat.chat_id)
            user = UserRepository.get(message.from_user.user_id)
            where_clauses = [
                Order.chat == chat,
                Order.user == user,
                Order.status == OrderStatus.NOT_CONFIRMED,
                Order.date.between(DateUtils.get_last_friday(), DateUtils.get_next_friday())
            ]

            OrderRepository.delete(where_clauses, number_rows=1, order_clause=Order.date.desc())
        except ResourceNotFoundException as ex:
            raise ex
