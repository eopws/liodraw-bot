from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot.config_reader import config


class IsAdminFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        print(message.chat.id)
        print(config.admin_chat_id)
        return self.is_admin == (message.chat.id == config.admin_chat_id)
