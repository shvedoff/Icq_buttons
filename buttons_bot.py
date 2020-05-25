import logging
from bot.bot import Bot
from buttons_logic import launch_handlers

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %I:%M:%S %p', level=logging.DEBUG)

TOKEN = ""

API_URL = "https://api.icq.net/bot/v1"


def main():
    bot = Bot(token=TOKEN, api_url_base=API_URL)
    launch_handlers(bot)
    bot.start_polling()


if __name__ == '__main__':
    main()
