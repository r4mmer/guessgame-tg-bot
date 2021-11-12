import logging
from collections import defaultdict
from random import randint

from telegram.ext import CallbackContext, Dispatcher

from .config import settings
from .utils import TooManyGuesses


logger = logging.getLogger(__name__)


class ChatData:
    """Custom class to persist chat game data"""
    def __init__(self) -> None:
        # create game
        self.guesses = defaultdict(int)
        self.secret = 0

    @property
    def is_started(self) -> bool:
        return bool(self.secret)

    def create_secret(self) -> None:
        self.secret = randint(1, settings.MAX_VALUE)
        logger.info("shh... the answer is {}".format(self.secret))

    def reset_guesses(self) -> None:
        self.guesses = defaultdict(int)

    def guess(self, user_id: int, value: int) -> bool:
        if not self.secret:
            # This will ignore any guesses if not started
            return False
        logger.debug("shh... the answer is {}".format(self.secret))
        if self.guesses[user_id] >= settings.MAX_GUESSES:
            raise TooManyGuesses('Too many guesses')
        self.guesses[user_id] += 1
        return self.secret == value

    def clear(self) -> bool:
        if not self.secret:
            return False
        self.secret = 0
        self.guesses = defaultdict(int)
        return True


class CustomContext(CallbackContext[dict, ChatData, dict]):
    """Custom class for context"""

    # start guess game
    def start_game(self) -> None:
        self.chat_data.reset_guesses()
        self.chat_data.create_secret()

    # stop guess game
    def stop_game(self) -> bool:
        return self.chat_data.clear()

    # reset guesses
    def reset_guesses(self) -> None:
        self.chat_data.reset_guesses()

    # guess a number
    #   - settings.MAX_GUESSES per user_id
    def guess(self, user_id: int, value: int) -> bool:
        return self.chat_data.guess(user_id, value)
