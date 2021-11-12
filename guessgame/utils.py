from typing import List

from telegram import ChatMember


class TooManyGuesses(Exception):
    pass


def is_admin(user_id: int, admins: List[ChatMember]):
    return user_id in [member.user.id for member in admins]
