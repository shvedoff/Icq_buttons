import json
import logging
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
from buttons_logic import CallbackLogic


TOKEN = ""

API_URL = "https://api.icq.net/bot/v1"


def main():
    bot = Bot(token=TOKEN, api_url_base=API_URL)
    logist = CallbackLogic(bot)
    bot.start_polling()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y.%m.%d %I:%M:%S %p',
                        level=logging.DEBUG)
    main()
