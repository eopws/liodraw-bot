from aiogram import Bot, Dispatcher
import asyncio

from bot.handlers import setup_routers
from bot.commandsworker import set_bot_commands

from bot.config_reader import config
from bot.blocklists import init_ban_list


async def main():
    init_ban_list()

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    from bot.utils.ban import parse_banned_list

    print(parse_banned_list())

    router = setup_routers()
    dp.include_router(router)

    # Регистрация /-команд в интерфейсе
    await set_bot_commands(bot)

    try:
        await bot.delete_webhook()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


asyncio.run(main())
 