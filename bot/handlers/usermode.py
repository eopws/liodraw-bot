from aiogram.types import Message, MediaGroup, ContentType
from typing import List
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


@dp.message_handler(is_admin=False, is_media_group=False, content_types=['photo'])
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

# @dp.message_handler(is_admin=False, is_media_group=True)#, content_types=['photo'])
@dp.message_handler(is_admin=False, is_media_group=True, content_types=ContentType.ANY)
async def supported_media(message: Message, album: List[Message]):
    """
    Хэндлер на группу медиафайлов от пользователя.
    Поддерживаются только типы, к которым можно добавить подпись (полный список см. в регистраторе внизу)
    :param message: медиафайлы от пользователя
    """
    if message.caption and len(message.caption) > 1000:
        return await message.reply("Слишком длинная подпись")
    if message.from_user.id in banned:
        return await message.answer("Вам запрещено отправлять сообщения!")

    given_caption = (message.caption or '') + get_user_info_string(message)

    media_group = MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": given_caption})
        except ValueError:
            return await message.answer("Тип альбома не поддерживается")

    await bot.send_media_group(
            config.admin_chat_id,
            media=media_group,
        )

    await bot.send_message(config.admin_chat_id, given_caption)


@dp.message_handler(is_admin=False, content_types=['text'])
async def text_message(message: Message):
    """
    Хэндлер на текстовые сообщения от пользователя
    :param message: сообщение от пользователя для админа(-ов)
    """

    if message.from_user.id in banned:
        await message.answer("Вам запрещено отправлять сообщения!")
    else:
        if len(message.text) > 4000:
            return await message.reply("Слишком большое сообщение")

        await bot.send_message(
            config.admin_chat_id,
            message.html_text + get_user_info_string(message), parse_mode="HTML"
        )
