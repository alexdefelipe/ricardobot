from datetime import date

import peewee as pw
from strenum import StrEnum

from ricardobot.services import translation_service
from ricardobot.persistance.models import BaseModel, Chat, User


class OrderStatus(StrEnum):
    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONFIRMED = "CONFIRMED"


class Order(BaseModel):
    order_id = pw.AutoField(column_name="order_id")
    chat = pw.ForeignKeyField(Chat, field=Chat.chat_id, backref='orders')
    user = pw.ForeignKeyField(User, field=User.user_id, backref='orders')
    first_part = pw.CharField()
    second_part = pw.CharField()
    drink = pw.CharField()
    status = pw.CharField()
    date = pw.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = OrderStatus.NOT_CONFIRMED
        self.date = date.today()

    def __str__(self):
        translation_params = {
            "first_part": self.first_part,
            "second_part": self.second_part,
            "drink": self.drink
        }
        return translation_service.get("ORDER_DESC", translation_params)
