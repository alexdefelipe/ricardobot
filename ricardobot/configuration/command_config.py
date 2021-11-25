from telebotify.models.message import Message

from ricardobot.services.bot_service import BotService
from ricardobot.utils.command_util import add_command


class CommandManager:
    commands = {}

    @staticmethod
    @add_command(commands, command="start")
    def on_start_command(bot: BotService, message: Message):
        bot.start_bot(message)

    @staticmethod
    @add_command(commands, command="mi_pedido")
    def on_my_order_command(bot: BotService, message: Message):
        bot.list_user_order(message)

    @staticmethod
    @add_command(commands, command="si")
    def confirm_order(bot: BotService, message):
        bot.confirm_order(message)

    @staticmethod
    @add_command(commands, command="no")
    def cancel_order(bot: BotService, message):
        bot.cancel_order(message)

    @staticmethod
    @add_command(commands, command="pedidos")
    def get_orders_report(bot: BotService, message: Message):
        bot.get_current_week_orders(message)

    @staticmethod
    @add_command(commands, command="subir_version")
    def upload_version(bot: BotService, message: Message):
        bot.upload_version(message)

    @staticmethod
    @add_command(commands, command="notificar_version")
    def notify_version(bot: BotService, message: Message):
        bot.notify_version(message)
