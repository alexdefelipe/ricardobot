import os
from typing import Dict, Callable, List

from peewee import DoesNotExist
from telebotify.bot_base import Bot
from telebotify.models.chat import Chat
from telebotify.models.message import Message
from telebotify.models.update import Update

from ricardobot.exceptions.resource_not_found_exception import ResourceNotFoundException
from ricardobot.persistance.models.order import OrderStatus
from ricardobot.persistance.repositories.chat_repository import ChatRepository
from ricardobot.persistance.repositories.user_repository import UserRepository
from ricardobot.services import translation_service
from ricardobot.services.order_service import OrderService
from ricardobot.services.version_service import VersionService
from ricardobot.utils.regex_util import RegexUtil


class BotService:
    def __init__(self,
                 api_key: str,
                 webhook_url: str,
                 command_handlers: Dict[str, Callable],
                 regex_handlers: Dict[str, Callable]):

        root_path = f"{os.environ['RICARDOBOT_ROOT_PATH']}"
        self.bot = Bot(api_key,
                       webhook_url=webhook_url,
                       commands=command_handlers,
                       cert_path=f"{root_path}/cert.pem")
        self.regex_handlers = regex_handlers

    def process_update(self, update_json: dict):
        update = Update.from_json(update_json)
        if update.update_id == self.bot.last_update_id:
            pass
        if update.message is not None and update.message.text is not None:
            self.check_command(update.message)
            self.bot.last_update_id = update.update_id
        if update.edited_message is not None and update.edited_message.text is not None:
            self.check_command(update.edited_message)
            self.bot.last_update_id = update.update_id

    def start_bot(self, message):
        self.bot.started = self.bot_already_started(message.chat)

        if self.bot.started:
            self.reply(message, translation_service.get("BOT_ALREADY_STARTED"))
        else:
            self.bot.started = True
            self.reply(message, translation_service.get("BOT_STARTED"))
            ChatRepository.create(message.chat.chat_id)

    @staticmethod
    def bot_already_started(chat: Chat) -> bool:
        try:
            ChatRepository.get(chat.chat_id)
            return True
        except DoesNotExist:
            return False

    def reply(self, message: Message, text):
        self.bot.send_message(message.chat.chat_id, text, reply_to_message_id=message.message_id)

    def check_command(self, message: Message) -> None:
        try:
            command = RegexUtil.apply_command_regex(message.text)
            if command is not None:
                self.run_command(command, message)
                pass
            if message.text is not None:
                self.run_regex_handlers(message)
        except Exception as ex:
            self.reply(message, f"No he podido procesar tu mensaje. Motivo: {ex}")

    def run_command(self, command, message) -> None:
        try:
            self.bot.commands[command](self, message)
        except KeyError as ex:
            self.reply(message, f"Command /{command} not defined. Use /help to get available commands")

    def run_regex_handlers(self, message: Message) -> List[str] or None:
        for regex, handler in self.regex_handlers.items():
            if not RegexUtil.regex_applies(regex, message.text):
                continue
            handler(self, message, RegexUtil.apply_regex(regex, message.text))
        return None

    def list_user_order(self, message: Message) -> None:
        self.bot.started = self.bot_already_started(message.chat)
        if not self.bot.started:
            self.reply(message, translation_service.get("BOT_NOT_STARTED_YET"))
            pass

        try:
            chat = ChatRepository.get(message.chat.chat_id)
            user = UserRepository.get_or_create(message.from_user, chat)
            order = OrderService.get_order(user, chat)
            translation_params = {
                "first_part": order.first_part,
                "second_part": order.second_part,
                "drink": order.drink
            }
            translation_message = "CONFIRMED_ORDER_REPORT" if order.status == OrderStatus.CONFIRMED else "NOT_CONFIRMED_ORDER_REPORT"
            order_report = translation_service.get(translation_message, translation_params)
            self.reply(message, order_report)
        except ResourceNotFoundException:
            self.reply(message, translation_service.get("NO_ORDER_YET"))

    def start_order(self, message: Message, params: List[str]) -> None:
        order = OrderService.start_order(message, params)
        translation_params = {
            "first_part": order.first_part,
            "second_part": order.second_part,
            "drink": order.drink
        }
        self.reply(message, translation_service.get("ORDER_CONFIRMATION", translation_params))

    def confirm_order(self, message: Message) -> None:
        try:
            OrderService.confirm_order(message)
            self.reply(message, translation_service.get("PERFECT"))
        except ResourceNotFoundException:
            self.reply(message, translation_service.get("CANT_CONFIRM_ORDER"))

    def cancel_order(self, message: Message) -> None:
        try:
            OrderService.cancel_order(message)
            self.reply(message, translation_service.get("PERFECT"))
        except ResourceNotFoundException:
            self.reply(message, translation_service.get("CANT_CANCEL_ORDER"))

    def get_current_week_orders(self, message: Message) -> None:
        try:
            orders = OrderService.get_current_week_orders(message)
            snacks = "\n".join([f"- {order.__str__()}" for order in orders])
            report = translation_service.get("ORDERS_REPORT", {"snacks": snacks})
            self.reply(message, report)
        except ResourceNotFoundException:
            self.reply(message, translation_service.get("NO_ORDERS_YET"))

    def upload_version(self, message: Message) -> None:
        try:
            VersionService.upload_version(message)
            self.reply(message, translation_service.get("PERFECT"))
        except ResourceNotFoundException:
            self.reply(message, translation_service.get("VERSION_ALREADY_EXISTS"))

    def notify_version(self, message: Message) -> None:
        version = VersionService.get_version(message)
        chats = ChatRepository.get_all()
        for chat in chats:
            self.bot.send_message(chat_id=chat.chat_id, text=version.changelog)
