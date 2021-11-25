import operator
from functools import reduce
from typing import List, Dict

from peewee import DoesNotExist

from ricardobot.exceptions.resource_not_found_exception import ResourceNotFoundException
from ricardobot.persistance.models import Order, Chat
from ricardobot.utils.date_utils import DateUtils


class OrderRepository:
    @staticmethod
    def get(order_id: int) -> Order:
        return Order.get(Order.order_id == order_id)

    @staticmethod
    def find_one(where_clauses: List = None) -> List[Order]:
        orders = Order.select().where(*where_clauses).limit(1)
        if len(orders) == 0:
            raise ResourceNotFoundException("Order", None)
        return orders

    @staticmethod
    def find(where_clauses: List = None) -> List[Order]:
        orders = Order.select().where(*where_clauses)
        if len(orders) == 0:
            raise ResourceNotFoundException("Order", None)
        return orders

    @staticmethod
    def find_all_by_chat(chat) -> List[Order]:
        return Order.select().where(Order.chat == chat)

    @staticmethod
    def create(order: Order) -> int:
        return Order.save(order)

    @staticmethod
    def update(update_clauses: Dict, where_clauses: List = None) -> None:
        query = (Order
                 .update(**update_clauses)
                 .where(*where_clauses))
        updated_rows = query.execute()

        if updated_rows == 0:
            raise ResourceNotFoundException("Order", None)

    @staticmethod
    def delete(where_clauses: List, **kwargs) -> None:
        try:
            query = (Order
                     .select()
                     .where(*where_clauses))
            if kwargs["order_clause"] is not None:
                query.order_by(kwargs["order_clause"])
            if kwargs["number_rows"] is not None:
                query.limit(kwargs["number_rows"])
            deleted_rows = query.get().delete_instance()

            if deleted_rows == 0:
                raise ResourceNotFoundException("Order", None)
        except DoesNotExist:
            raise ResourceNotFoundException("Order", None)
