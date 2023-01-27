from aiogram.types import Message


def get_user_info_string(message: Message):
    """
    Выдает строку с информацией о пользователе
    :return: string
    """
    return f"\n\n#имя_{message.from_user.first_name}, #id{message.from_user.id}"


def extract_id(message: Message) -> int:
    """
    Извлекает ID юзера из хэштега в сообщении
    :param message: сообщение, из хэштега в котором нужно достать айди пользователя
    :return: ID пользователя, извлечённый из хэштега в сообщении
    """
    # Получение списка сущностей (entities) из текста или подписи к медиафайлу в отвечаемом сообщении
    entities = message.entities or message.caption_entities
    # Если всё сделано верно, то последняя (или единственная) сущность должна быть хэштегом...
    if not entities or entities[-1].type != "hashtag":
        raise ValueError("Не удалось извлечь ID для ответа!")

    # ... более того, хэштег должен иметь вид #id123456, где 123456 — ID получателя
    hashtag = entities[-1].get_text(message.text or message.caption) # extract(message.text or message.caption)
    if len(hashtag) < 4 or not hashtag[3:].isdigit():  # либо просто #id, либо #idНЕЦИФРЫ
        raise ValueError("Некорректный ID для ответа!")

    return int(hashtag[3:])


def extract_name(message: Message) -> str:
    """
    Извлекает имя юзера из хэштега в сообщении
    :param message: сообщение, из хэштега в котором нужно достать имя пользователя
    :return: имя пользователя, извлечённый из хэштега в сообщении
    """

    # Получение списка сущностей (entities) из текста или подписи к медиафайлу в отвечаемом сообщении
    entities = message.entities or message.caption_entities

    # Если всё сделано верно, то предпоследняя (последняя - id) сущность должна быть хэштегом...
    if not entities or entities[-2].type != "hashtag":
        raise ValueError("Не удалось извлечь имя для ответа!")

    # ... более того, хэштег должен иметь вид #имя_ЗНАЧЕНИЕ, где ЗНАЧЕНИЕ — имя получателя
    hashtag = entities[-2].extract(message.text or message.caption)
    if len(hashtag) < 6:  # просто #имя_
        raise ValueError("Некорректное имя для ответа!")

    return hashtag[5:]
