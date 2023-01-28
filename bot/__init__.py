import os
from os.path import dirname

ROOT_PATH=dirname(os.path.abspath("./__main__.py"))

from aiogram import executor
from bot.dispatcher import dp
from bot.blocklists import init_ban_list
import bot.handlers # init handlers

def start():
    init_ban_list()

    executor.start_polling(dp, skip_updates=False)
