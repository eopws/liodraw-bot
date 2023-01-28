from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from bot.config_reader import config


async def set_default_commands(dp: Dispatcher):
    admin_commands = [
        BotCommand(command="ban", description="Заблокировать пользователя"),
        BotCommand(command="unban", description="Разблокировать пользователя"),
        BotCommand(command="list_banned", description="Список заблокированных"),
        BotCommand(command="help", description="Справка по использованию бота")
    ]

    await dp.bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=config.admin_chat_id))

    user_commands = [
        BotCommand(command="help", description="Справка по использованию бота")
    ]

    await dp.bot.set_my_commands(commands=user_commands, scope=BotCommandScopeDefault())
