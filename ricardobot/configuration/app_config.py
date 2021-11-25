import os

from flask import Flask

from ricardobot.services.bot_service import BotService

app = Flask(__name__)

from ricardobot.configuration import command_manager, regex_manager

bot = BotService(os.environ["BOT_KEY"],
                 webhook_url="https://intelihealthia.ddns.net:8443/main",
                 command_handlers=command_manager.commands,
                 regex_handlers=regex_manager.regex_handlers)
