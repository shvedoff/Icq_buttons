import json
import time
import string
import logging
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
from bot.filter import Filter
from random import randrange, choice, random
default_markup = [
    [{"text": "Все действия с кнопками", "callbackData": "types"}],
    [{"text": "Маленькие кнопки", "callbackData": "micro_buttons"}],
    [{"text": "Все типы медиа", "callbackData": "all_media"}],
    [{"text": "Длинный текст в кнопке", "callbackData": "all_long"}],
    [{"text": "С переносом строки", "callbackData": "newline"}],
    [{"text": "Своя конфигурация", "callbackData": "custom_intro"}],
    [{"text": "Сообщение, которое можно отредактировать",
        "callbackData": "edit_intro"}],
    [{"text": "Все типы стилей", "callbackData": "styles"}],
    [{"text": "Рандом...", "callbackData": "rand"}],
]
edit_text = ('Жми!', [[{"text": "Жми!", "callbackData": "edit"}]])

styles_all = ('Все типы стилей', [
    [{"text": "primary style", "callbackData": "nothing", "style": "primary"}],
    [{"text": "attention style", "callbackData": "nothing",
        "style": "attention"}],
    [{"text": "base style", "callbackData": "nothing", "style": "base"}],
])

custom_intro_text = 'Напиши текст в формате: AxB text, чтобы получить сетку\
 кнопок размера A на B c тектом text. Пример: 2x3 привет '

all_types_answer = ('Все типы кнопок', [
    [{"text": "Callback: Nothing", "callbackData": "no_callback"}],
    [{"text": "Callback: Toast", "callbackData": "toast"}],
    [{"text": "Callback: Alert", "callbackData": "alert"}],
    [{"text": "Callback: Url", "callbackData": "url"}],
    [{"text": "Callback: Alert+Url", "callbackData": "alert_url"}],
    [{"text": "Callback: Toast+Url", "callbackData": "toast_url"}],
    [{"text": "Only Url", "url": "http://mail.ru"}],
])

newline_text = ("С переносом строки", [
    [{"text": "Hello", "callbackData": "nothing"},
     {"text": "hello\nolleh", "callbackData": "nothing"},
     {"text": "Привет", "callbackData": "nothing"}]
])

types_list = {
    "text": "текст",
    "longtext": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad \
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex\
    ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate \
    velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat\
    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id \
    est laborum.",
    "photo": "https://files.icq.net/get/0jmjm00050gDpoit4ZDA2B5e6b480a1ac",
    "photo2": "https://files.icq.net/get/063c60006MEvtsURDaPvaW5e6b8b951ac",
    "video": "https://files.icq.net/get/8akak0008BfM3IFsSs4qwf5e67861f1bc",
    "gif": "https://media.giphy.com/media/l2R0aKwejYr8ycKAg/giphy.gif",
    "url": "https://www.mail.ru",
    "profile": "https://icq.im/stickers_bot",
    "sticker": "https://files.icq.net/get/28Ialp8YPunsdcuLpIixxk5a2fe49e1af",
    "ptt": "https://files.icq.net/get/I0006DFE9MCGf1vdkUBZCs570bc6701bf"
}
long_text_on_button_markup = [[{"text": "Lorem ipsum dolor sit amet, \
consectetur adipiscing elit, sed do eiusmod tempor incididunt ut\
labore et dolore magna aliqua.", "callbackData": "nothing"}]]
text_on_button_markup = [[{"text": "Lorem", "callbackData": "nothing"}]]


def sender(bot, chat_id=None, query_id=None, markup=None, message='', text='',
           alert=False, url='', separate_message=''):
    logging.info(f'Invoked sender with args: {locals()}')
    if separate_message:
        bot.send_text(chat_id=chat_id,
                      text=separate_message)
    if markup:
        bot.send_text(chat_id=chat_id,
                      text=message,
                      inline_keyboard_markup=json.dumps(markup))
    if query_id:
        bot.answer_callback_query(
            query_id=query_id,
            text=text,
            show_alert=alert,
            url=url)


def toast(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           text='toast',  separate_message='toast pressed',
           )


def alert(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           text='alert', alert=True, separate_message='alert pressed',
           )


def url(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           url='http://mail.ru', separate_message='url pressed',
           )


def alert_url(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           url='http://mail.ru', alert='true',
           separate_message='all_types pressed',
           )


def toast_url(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           text='Toast', url='http://mail.ru',
           separate_message='all_types pressed',
           )


def types(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           message=all_types_answer[0], markup=all_types_answer[1],
           separate_message='all_types pressed',
           )


def styles(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           message=styles_all[0], markup=styles_all[1],
           separate_message='styles_all pressed',
           )


def newline(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           message=newline_text[0], markup=newline_text[1],
           separate_message='newline pressed.',
           )


def custom_intro(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           separate_message=custom_intro_text)


def edit_intro(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           message=edit_text[0], markup=edit_text[1],
           separate_message='edit_intro pressed.',
           )


def edit(bot, event):
    text = "Отредактировано!"+str(time.time())
    markup = [[{'text': "Отредактировано!", 'callbackData': "nothing"}]]
    bot.edit_text(chat_id=event.data['message']['chat']['chatId'],
                  msg_id=event.data['message']['msgId'], text=text,
                  inline_keyboard_markup=json.dumps(markup))

    sender(bot, chat_id=event.data['message']['chat']
           ['chatId'], query_id=event.data['queryId'])


def get_answer_by_text(bot, event):
    text = event.text
    answer = 'Привет!'
    markup = default_markup

    if 'x' in text:
        custom(bot, event, text)
    sender(bot, chat_id=event.from_chat, message=answer,
           markup=markup)


def nothing(bot, event):
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'],
           separate_message='nothing pressed')


def callbacks_with_all_prefix(bot, event):
    callback = event.data['callbackData']
    sender(bot, chat_id=event.data['message']['chat']
           ['chatId'], separate_message=f'{callback} pressed',)

    postfix = callback[4:]
    info_on_callback = postfix.split('_')
    reply = []
    if info_on_callback[0] == 'long':
        button = long_text_on_button_markup
        callback_for_buttons = 'all_long_'
    else:
        button = text_on_button_markup
        callback_for_buttons = 'all_media_'

    if len(info_on_callback) == 1:
        buttons = [
            [{"text": 'Все', "callbackData": callback_for_buttons+"all"}]]
        for key in types_list.keys():
            buttons.append(
                [{"text": key, "callbackData": callback_for_buttons+key}])
        reply.append({'text': 'есть такие:', 'markup': buttons})
    else:
        if info_on_callback[1] == 'all':
            reply = []
            for type in types_list.keys():
                reply.append({'text': types_list[type], 'markup': button,
                              'alert': False, 'url': ''})
        else:

            reply.append({'text': types_list[info_on_callback[1]],
                          'markup': button, 'alert': False, 'url': ''})

    if reply:
        for part in reply:
            sender(bot, chat_id=event.data['message']['chat']['chatId'],
                   query_id=event.data['queryId'], markup=part['markup'],
                   message=part['text'])


def rand(bot, event):
    lines_count = randrange(13)+1
    markup = []

    for i in range(lines_count):
        colls_count = randrange(8)+1
        lines = []
        for j in range(colls_count):
            button = {}
            string_on_button = ''
            for k in range(randrange(6)+1):
                lower_upper_alphabet = string.ascii_letters
                string_on_button += choice(lower_upper_alphabet)
                if random() > 0.8:
                    string_on_button += '\n'

            button['text'] = string_on_button.strip()
            button['callbackData'] = "nothing"
            button['style'] = choice(["primary", "attention", "base"])
            lines.append(button)
        markup.append(lines)

    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'], markup=markup,
           message="Нарандомилось:", separate_message='random pressed.')


def custom(bot, event, text):
    text_on_buttons = "a"
    try:
        text = text.split(' ')
        if len(text) > 1:
            text_on_buttons = text[1]
        second = int(text[0][:text[0].find('x')])
        first = int(text[0][text[0].find('x')+1:])
    except Error as e:
        logger.exception(e)
        first = 8
        second = 1
    buttons = [
        [{'text': text_on_buttons, 'callbackData': "nothing"}]*first]*second

    sender(bot, chat_id=event.from_chat,
           markup=buttons, message="Своя конфигурация:",
           separate_message='custom entered.')


def small_buttons(bot, event):
    buttons = [
        [{'text': 'a', 'callbackData': "nothing"}]*8]*1
    sender(bot, chat_id=event.data['message']['chat']['chatId'],
           query_id=event.data['queryId'], markup=buttons,
           message="Маленькие кнопки:",
           separate_message='small _buttons entered.')


def launch_handlers(bot):
    bot.dispatcher.add_handler(MessageHandler(callback=get_answer_by_text))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=types, filters=Filter.callback_data("types")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=callbacks_with_all_prefix,
        filters=Filter.callback_data_regexp("all.*")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=rand, filters=Filter.callback_data("rand")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=newline, filters=Filter.callback_data("newline")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=custom_intro, filters=Filter.callback_data("custom_intro")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=styles, filters=Filter.callback_data("styles")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=nothing, filters=Filter.callback_data("nothing")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=toast, filters=Filter.callback_data("toast")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=alert, filters=Filter.callback_data("alert")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=url, filters=Filter.callback_data("url")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=alert_url, filters=Filter.callback_data("alert_url")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=toast_url, filters=Filter.callback_data("toast_url")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=edit, filters=Filter.callback_data("edit")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
        callback=edit_intro, filters=Filter.callback_data("edit_intro")))
    bot.dispatcher.add_handler(BotButtonCommandHandler(
            callback=small_buttons,
            filters=Filter.callback_data("micro_buttons")))
