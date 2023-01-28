from aiogram import Bot, Dispatcher
from bot.filters import SupportedMediaFilter, IsAdminFilter
from bot.config_reader import config
from bot.middleware.AlbumMiddleware import AlbumMiddleware
from bot.commandsworker import set_default_commands

import asyncio


# prerequisites
if not config.bot_token.get_secret_value():
    print("No token provided")
    exit("No token provided")

print(config.bot_token.get_secret_value())

# init
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher(bot)

loop = asyncio.get_event_loop()
loop.create_task(set_default_commands(dp))

# middlewares
dp.middleware.setup(AlbumMiddleware())

# activate filters
dp.filters_factory.bind(SupportedMediaFilter)
dp.filters_factory.bind(IsAdminFilter)
