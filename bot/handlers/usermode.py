from aiogram import Bot
from aiogram.types import Message
from bot.blocklists import banned

from bot.dispatcher import dp, bot

from bot.utils.strings import get_user_info_string

from bot.config_reader import config


@dp.message_handler(is_admin=False, commands="start", commands_prefix="/")
async def cmd_start(message: Message):
    """
    Приветственное сообщение от бота пользователю
    :param message: сообщение от пользователя с командой /start
    """
    await message.answer("Привет")


@dp.message_handler(is_admin=False, commands="help", commands_prefix="/")
async def cmd_help(message: Message):
    """
    Справка для пользователя
    :param message: сообщение от пользователя с командой /help
    """
    await message.answer("Это бот для общения с администрацией канала, все сообщения которые вы присылаете мне будут пересланы администрации")


@dp.message_handler(is_admin=False)
async def text_message(message: Message):
    """
    Хэндлер на текстовые сообщения от пользователя
    :param message: сообщение от пользователя для админа(-ов)
    """
    print('message')
    if message.from_user.id in banned:
        await message.answer("Вам запрещено отправлять сообщения!")
    else:
        print(f'{message.from_user.id} отправляет сообщение')
        if len(message.text) > 4000:
            return await message.reply("Слишком большое сообщение")

        await bot.send_message(
            config.admin_chat_id,
            message.html_text + get_user_info_string(message), parse_mode="HTML"
        )


@dp.message_handler(is_admin=False)
async def supported_media(message: Message):
    """
    Хэндлер на медиафайлы от пользователя.
    Поддерживаются только типы, к которым можно добавить подпись (полный список см. в регистраторе внизу)
    :param message: медиафайл от пользователя
    """
    if message.caption and len(message.caption) > 1000:
        return await message.reply("Слишком длинная подпись")
    if message.from_user.id in banned:
        await message.answer("Вам запрещено отправлять сообщения!")
    else:
        await message.copy_to(
            config.admin_chat_id,
            caption=((message.caption or "") + get_user_info_string(message)),
            parse_mode="HTML"
        )
