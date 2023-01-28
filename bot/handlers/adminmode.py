from aiogram.types import Message, MediaGroup, ContentType
from bot.dispatcher import dp, bot

from bot.utils.strings import extract_id
from typing import List


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


@dp.message_handler(is_admin=True, is_media_group=False, content_types=['photo', 'audio', 'video', 'document', 'voice', 'animation', 'video_note'])
async def supported_media(message: Message):
    """
    Хэндлер на медиафайлы от пользователя.
    Поддерживаются только типы, к которым можно добавить подпись (полный список см. в регистраторе внизу)
    :param message: медиафайл от пользователя
    """
    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    if message.caption and len(message.caption) > 1000:
        return await message.reply("Слишком длинная подпись")
    else:
        try:
            user_id = extract_id(message.reply_to_message)

            await message.copy_to(
                user_id,
                caption=((message.caption or "")),
                parse_mode="HTML"
            )
        except:
            await message.reply("Не получилось ответить пользователю :(")
        user_id = extract_id(message.reply_to_message)


@dp.message_handler(is_admin=True, is_media_group=True, content_types=ContentType.ANY)
async def supported_media(message: Message, album: List[Message]):
    """
    Хэндлер на группу медиафайлов от пользователя.
    Поддерживаются только типы, к которым можно добавить подпись (полный список см. в регистраторе внизу)
    :param message: медиафайлы от пользователя
    """

    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    is_first_message = True

    media_group = MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # Добавляем подпись только к первой картинке, чтобы она отображалась под сообщением
            if is_first_message:
                given_caption = message.caption or ''
                media_group.attach({"media": file_id, "type": obj.content_type, "caption": given_caption})
                is_first_message = False
            else:
                media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("Тип альбома не поддерживается")
 
    try:
        user_id = extract_id(message.reply_to_message)

        await bot.send_media_group(
                user_id,
                media=media_group,
                # caption=((message.caption or "") + get_user_info_string(message)),
            )
    except:
        await message.reply("Не получилось ответить пользователю :(")
    user_id = extract_id(message.reply_to_message)


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


@dp.message_handler(is_admin=True, content_types=['sticker'])
async def sticker_message(message: Message):
    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    # Вырезаем ID
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    await bot.send_sticker(
        chat_id=user_id,
        sticker=message.sticker.file_id
    )
