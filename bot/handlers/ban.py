from contextlib import suppress
from aiogram.types import Message

from bot.dispatcher import dp

from bot.blocklists import ban_user, unban_user, banned
from bot.utils.strings import extract_id, extract_name


@dp.message_handler(is_admin=True, commands="ban", commands_prefix="/")
async def cmd_ban(message: Message):
    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    ban_user(int(user_id))

    try:
        user_name = extract_name(message.reply_to_message)
        await message.reply(f"{user_name} забанен")
    except:
        await message.reply(f"{user_id} забанен")


@dp.message_handler(is_admin=True, commands="unban", commands_prefix="/")
async def cmd_unban(message: Message):
    if not message.reply_to_message:
        await message.reply("Ошибка: Нужно ответить на сообщение")
        return

    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    user_id = int(user_id)
    # with suppress(KeyError):
    unban_user(user_id)

    try:
        user_name = extract_name(message.reply_to_message)
        await message.reply(f"{user_name} разблокирован")
    except:
        await message.reply(f"{user_id} разблокирован")


@dp.message_handler(is_admin=True, commands="list_banned", commands_prefix="/")
async def cmd_list_banned(message: Message):
    has_bans = len(banned) > 0
    if not has_bans:
        await message.answer("Никто не заблокирован")
        return
    result = []
    if len(banned) > 0:
        result.append("Список заблокированных пользователей:")
        for item in banned:
            result.append(f"• #id{item}")

    await message.answer("\n".join(result))
