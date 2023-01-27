from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType, Message

from bot.utils.strings import extract_id

router = Router()
router.message.filter(F.chat.id == 1551500575)


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    """
    Справка для админа
    :param message: сообщение от пользователя с командой /help
    """
    await message.answer("""
        Это бот для общения с пользователями канала, все сообщения которые пользователи присылают мне будут пересланы вам.
        Чтобы написать пользователю от имени бота, напишите ответ на сообщение, он будет переслан автору
    """)


@router.message(F.reply_to_message)
async def reply_to_user(message: Message):
    """
    Ответ администратора на сообщение юзера (отправленное ботом).
    Используется метод copy_message, поэтому ответить можно чем угодно, хоть опросом.
    :param message: сообщение от админа, являющееся ответом на другое сообщение
    """

    # Вырезаем ID
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    # Пробуем отправить копию сообщения.
    # В теории, это можно оформить через errors_handler, но мне так нагляднее
    try:
        await message.copy_to(user_id)
    except TelegramAPIError as ex:
        await message.reply("Не получилось ответить пользователю :(")


@router.message(~F.reply_to_message)
async def has_no_reply(message: Message):
    """
    Хэндлер на сообщение от админа, не содержащее ответ (reply).
    В этом случае надо кинуть ошибку.
    :param message: сообщение от админа, не являющееся ответом на другое сообщение
    """
    if message.content_type not in (ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER):
        await message.reply("Ошибка: Нужно ответить на сообщение")

