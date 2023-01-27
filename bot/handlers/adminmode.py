from aiogram.types import Message
from aiogram.types import Message

from bot.dispatcher import dp

from bot.utils.strings import extract_id

@dp.message_handler(is_admin=True, commands="start", commands_prefix="/")
async def cmd_help(message: Message):
    """
    Справка для админа
    :param message: сообщение от пользователя с командой /help
    """
    await message.answer("""
        Это бот для общения с пользователями канала, все сообщения которые пользователи присылают мне будут пересланы вам.
        Чтобы написать пользователю от имени бота, напишите ответ на сообщение, он будет переслан автору
    """)


@dp.message_handler(is_admin=True)
async def reply_to_user(message: Message):
    """
    Ответ администратора на сообщение юзера (отправленное ботом).
    Используется метод copy_message, поэтому ответить можно чем угодно, хоть опросом.
    :param message: сообщение от админа, являющееся ответом на другое сообщение
    """

    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    # Вырезаем ID
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    # Пробуем отправить копию сообщения.
    # В теории, это можно оформить через errors_handler, но мне так нагляднее
    try:
        await message.copy_to(user_id)
    except:
        await message.reply("Не получилось ответить пользователю :(")
