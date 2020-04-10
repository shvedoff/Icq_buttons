import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
from buttons_logic import CollbackLogic


TOKEN = ""

API_URL = "https://api.icq.net/bot/v1"


def main():
    bot = Bot(token=TOKEN,   api_url_base=API_URL)
    logist = CollbackLogic()

    def message_cb(bot, event):
        answer_params = logist.get_answer_by_text(event.text)
        bot.send_text(chat_id=event.from_chat, text=answer_params['text'],
                      inline_keyboard_markup=json.dumps(answer_params['markup']))

    def buttons_answer_cb(bot, event):
        answers = logist.get_answer_by_callback(event)

        if type(answers) != list:
            answers = [answers]

        for answer_params in answers:
            if 'edit' in answer_params:
                bot.edit_text(chat_id=event.data['message']['chat']['chatId'],
                msg_id=event.data['message']['msgId'],text=answer_params['text'],
                inline_keyboard_markup=json.dumps(answer_params['markup']))
                bot.answer_callback_query(
                    query_id=event.data['queryId'], text='',
                    show_alert=False,  url='')
            elif answer_params['markup'] != []:

                bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                              text=answer_params['text'],
                              inline_keyboard_markup=json.dumps(answer_params['markup']))
                bot.answer_callback_query(
                    query_id=event.data['queryId'], text='',
                    show_alert=False,  url='')
            else:
                bot.answer_callback_query(
                    query_id=event.data['queryId'],
                    text=answer_params['text'],
                    show_alert=answer_params['alert'],
                    url=answer_params['url'])
            if 'message' in answer_params:
                bot.send_text(
                    chat_id=event.data['message']['chat']['chatId'],
                    text=answer_params['message'])

    bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(callback=buttons_answer_cb))
    bot.start_polling()


if __name__ == '__main__':

    main()
