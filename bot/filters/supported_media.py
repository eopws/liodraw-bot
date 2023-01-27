from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ContentType


class SupportedMediaFilter(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.content_type in (
            ContentType.ANIMATION, ContentType.AUDIO, ContentType.DOCUMENT,
            ContentType.PHOTO, ContentType.VIDEO, ContentType.VOICE
        )
