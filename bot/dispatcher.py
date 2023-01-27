from aiogram import Bot, Dispatcher
from bot.filters import SupportedMediaFilter, IsAdminFilter
from bot.config_reader import config


# prerequisites
if not config.bot_token.get_secret_value():
    exit("No token provided")

# init
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(SupportedMediaFilter)
dp.filters_factory.bind(IsAdminFilter)
