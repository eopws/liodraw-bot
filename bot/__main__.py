from aiogram import executor
from bot.dispatcher import dp
from bot.blocklists import init_ban_list
import bot.handlers # init handlers


init_ban_list()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
