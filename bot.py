import logging

from guessgame import configure_updater
from guessgame.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('Startup...')

    updater = configure_updater()

    logger.info(settings.PORT)
    logger.info(settings)

    if settings.WEBHOOK_URL:
        updater.start_webhook(listen="0.0.0.0", port=settings.PORT, url_path=settings.TOKEN)
        updater.bot.setWebhook(settings.WEBHOOK_URL + settings.TOKEN)
    else:
        updater.start_polling()
    # stop with ctrl-c or one of (SIGINT, SIGTERM, SIGABRT) to the updater process
    updater.idle()

if __name__ == '__main__':
    main()
