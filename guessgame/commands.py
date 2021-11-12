from typing import Dict
import logging

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ContextTypes

from .config import settings
from .context import CustomContext, ChatData
from .utils import is_admin, TooManyGuesses

logger = logging.getLogger(__name__)


def start(update: Update, context: CustomContext) -> None:
    """ Start a game in the caller chat
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    # check admin priviledges and start
    if is_admin(user_id, update.effective_chat.get_administrators()):
        context.start_game()
        # context.bot.send_message(chat_id=chat_id, text="The game has started! Make your guesses with /guess")
        context.bot.send_message(chat_id=chat_id, text=f"""**Guess Game**

# *Rules*

A random number was generated between 1-{settings.MAX_VALUE}, first one to guess correctly, wins.

Anyone can guess with the command:
"`/guess 123`"
(123 being your guess).

{settings.MAX_GUESSES} guesses per user,

A chat admin can issue a
`/reset_guesses`
The generated number doesn't change but everyone can guess {settings.MAX_GUESSES} more times

Good luck, aaaand... BEGIN!""", parse_mode=ParseMode.MARKDOWN)


def stop(update: Update, context: CustomContext) -> None:
    """ Stop a game
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    # check admin priviledges and start
    if not is_admin(user_id, update.effective_chat.get_administrators()):
        return

    if not context.chat_data.is_started:
        update.message.reply_text(text="No active game!")
        return
    context.stop_game()
    # update.message.reply_text(text="Game was stopped!")
    context.bot.send_message(chat_id=chat_id, text="Game was stopped!")


def reset_guesses(update: Update, context: CustomContext) -> None:
    """ Reset guesses for a chat
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    # check admin priviledges and start
    if not is_admin(user_id, update.effective_chat.get_administrators()):
        return
    if not context.chat_data.is_started:
        update.message.reply_text(text="The game hasn't started...")
        return
    context.reset_guesses()
    context.bot.send_message(chat_id=chat_id, text="Guess count reset, everyone can try again!!!")


def guess(update: Update, context: CustomContext) -> None:
    """
    """
    user_id = update.effective_user.id

    if not context.chat_data.is_started:
        update.message.reply_text(text="No active game...")
        return
    message = update.effective_message.text
    t = message.replace('/guess', '').strip()
    try:
        int(t)
    except ValueError:
        # invalid guess
        update.effective_message.delete()
        return
    value = int(t)
    logger.info("A guess of {}".format(value))
    correct = False
    try:
        correct = context.guess(user_id, value)
    except TooManyGuesses:
        # too many guesses
        update.effective_message.delete()
        return

    if correct:
        context.stop_game()
        # stop cat gif
        file_id = "CgACAgEAAxkBAAMsYYp3DzC6dOQWwzrq7qqitylrongAArQBAAKR5kBE3bwvxsksygUiBA"
        update.effective_message.reply_animation(file_id)
        # update.effective_message.reply_text(text="WINNER WINNER CHICKEN DINNER!!!")


def configure_updater() -> Updater:
    context_types = ContextTypes(context=CustomContext, chat_data=ChatData)
    updater = Updater(settings.TOKEN, context_types=context_types)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(CommandHandler('reset_guesses', reset_guesses))
    dispatcher.add_handler(CommandHandler('guess', guess))

    return updater
