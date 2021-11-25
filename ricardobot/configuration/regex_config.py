from typing import List

from telebotify.models.message import Message
from ricardobot.services.bot_service import BotService
from ricardobot.utils.regex_util import START_ORDER_REGEX, add_regex


class RegexManager:
    regex_handlers = {}

    @staticmethod
    @add_regex(regex_handlers, regex=START_ORDER_REGEX)
    def on_start_order_regex(bot: BotService, message: Message, params: List[str]):
        bot.start_order(message, params)
