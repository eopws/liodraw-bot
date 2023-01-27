from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from bot.blocklists import banned

from bot.filters import SupportedMediaFilter
from bot.utils.strings import get_user_info_string

from bot.config_reader import config


router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    """
    Приветственное сообщение от бота пользователю
    :param message: сообщение от пользователя с командой /start
    """
    await message.answer("Привет")

@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    """
    Справка для пользователя
    :param message: сообщение от пользователя с командой /help
    """
    await message.answer("Это бот для общения с администрацией канала, все сообщения которые вы присылаете мне будут пересланы администрации")



@router.message(F.text)
async def text_message(message: Message, bot: Bot):
    """
    Хэндлер на текстовые сообщения от пользователя
    :param message: сообщение от пользователя для админа(-ов)
    """
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

@router.message(SupportedMediaFilter())
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