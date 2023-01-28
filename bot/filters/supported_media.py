from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, ContentType


class SupportedMediaFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_media_message"

    def __init__(self, is_media_message: bool):
        self.is_media_message = is_media_message

    async def check(self, message: Message) -> bool:
        return self.is_media_message == message.content_type in (
            ContentType.ANIMATION, ContentType.AUDIO, ContentType.DOCUMENT,
            ContentType.PHOTO, ContentType.VIDEO, ContentType.VOICE
        )
