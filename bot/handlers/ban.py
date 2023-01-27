from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.blocklists import ban_user, unban_user, banned
from bot.config_reader import config
from bot.utils.strings import extract_id, extract_name


router = Router()
router.message.filter(F.chat.id == config.admin_chat_id)


@router.message(Command(commands=["ban"]), F.reply_to_message)
async def cmd_ban(message: Message, bot: Bot):
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))

    ban_user(int(user_id))
    print(f'{user_id} is being banned')

    try:
        user_name = extract_name(message.reply_to_message)
        await message.reply(f"{user_name} забанен")
    except:
        await message.reply(f"{user_id} забанен")


@router.message(Command(commands=["unban"]), F.reply_to_message)
async def cmd_unban(message: Message):
    try:
        user_id = extract_id(message.reply_to_message)
    except ValueError as ex:
        return await message.reply(str(ex))
    user_id = int(user_id)
    with suppress(KeyError):
        unban_user(user_id)

    try:
        user_name = extract_name(message.reply_to_message)
        await message.reply(f"{user_name} разблокирован")
    except:
        await message.reply(f"{user_id} разблокирован")


@router.message(Command(commands=["list_banned"]))
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
