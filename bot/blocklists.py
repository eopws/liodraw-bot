from bot.utils.ban import *

banned = set()


def init_ban_list():
    banned_users = parse_banned_list()

    for user in banned_users:
        banned.add(int(user))

def ban_user(user_id: int):
    banned.add(user_id)

    add_to_banned_list(str(user_id))

def unban_user(user_id: int):
    banned.remove(user_id)

    remove_from_banned_list(str(user_id))
