from aiogram import Bot, Dispatcher
from bot.filters import SupportedMediaFilter, IsAdminFilter
from bot.config_reader import config
from bot.middleware.AlbumMiddleware import AlbumMiddleware


# prerequisites
if not config.bot_token.get_secret_value():
    print("No token provided")
    exit("No token provided")

print('starting')

# init
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher(bot)

# middlewares
dp.middleware.setup(AlbumMiddleware())

# activate filters
dp.filters_factory.bind(SupportedMediaFilter)
dp.filters_factory.bind(IsAdminFilter)
