import json
import time
import string
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
from random import randrange, choice, random

default_markup = [
    [{"text": "Все действия с кнопками", "callbackData": "all_types"}],
    [{"text": "Маленькие кнопки", "callbackData": "8x1"}],
    [{"text": "Все типы медиа", "callbackData": "all_media"}],
    [{"text": "Длинный текст в кнопке", "callbackData": "all_long"}],
    [{"text": "С переносом строки", "callbackData": "newline"}],
    [{"text": "Своя конфигурация", "callbackData": "custom"}],
    [{"text": "Сообщение, которое можно отредактировать",
        "callbackData": "redact"}],
    [{"text": "Все типы стилей", "callbackData": "styles"}],
    [{"text": "Рандом...", "callbackData": "rand"}],
]
redact = ('Жми!', [[{"text": "Жми!", "callbackData": "edit"}]])

styles = ('Все типы стилей', [
    [{"text": "primary style", "callbackData": "nothing", "style": "primary"}],
    [{"text": "attention style", "callbackData": "nothing",
        "style": "attention"}],
    [{"text": "base style", "callbackData": "nothing", "style": "base"}],
])

custom = 'Напиши текст в формате: AxB text, чтобы получить сетку кнопок \
размера A на B c тектом text. Пример: 2x3 привет '

all_types = ('Все типы кнопок', [
    [{"text": "Callback: Nothing", "callbackData": "nothing"}],
    [{"text": "Callback: Toast", "callbackData": "toast"}],
    [{"text": "Callback: Alert", "callbackData": "alert"}],
    [{"text": "Callback: Url", "callbackData": "url"}],
    [{"text": "Callback: Alert+Url", "callbackData": "alert_url"}],
    [{"text": "Callback: Toast+Url", "callbackData": "toast_url"}],
    [{"text": "Only Url", "url": "http://mail.ru"}],
])

newline = ("С переносом строки", [
    [{"text": "Hello", "callbackData": "nothing"},
     {"text": "hello\nolleh", "callbackData": "nothing"},
     {"text": "Привет", "callbackData": "nothing"}]
])

types = {
    "text": "текст",
    "longtext": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed  \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad  \
    minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex \
    ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate  \
    velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat \
    cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id  \
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


def all(callback):
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
        for key in types.keys():
            buttons.append(
                [{"text": key, "callbackData": callback_for_buttons+key}])
    else:

        if info_on_callback[1] == 'all':
            reply = []
            for type in types.keys():
                reply.append({'text': types[type],'markup': button,
                    'alert': False,'url': ''})
        else:

            reply = {'text': types[info_on_callback[1]],'markup': button,
                'alert': False,'url': ''}

    if reply:
        return reply
    return {'alert': False, 'text': "есть такие:", 'url': '', 'markup': buttons,
     'message': "all media pressed."}


def rand():
    lines_count = randrange(14)
    callback = []

    for i in range(lines_count):
        colls_count = randrange(9)
        lines = []
        for j in range(colls_count):
            button = {}
            string_on_button = ''
            for k in range(randrange(6)):
                lower_upper_alphabet = string.ascii_letters
                string_on_button += choice(lower_upper_alphabet)
                if random() > 0.8:
                    string_on_button += '\n'

            button['text'] = string_on_button.strip()
            button['callbackData'] = "nothing"
            button['style'] = choice(["primary", "attention", "base"])
            lines.append(button)
        callback.append(lines)
    return {'alert': False, 'text': "Нарандомилось:", 'url': '',
     'markup': callback, 'message': 'random pressed.'}


def custom(text):
    text_on_buttons = "a"
    try:
        text = text.split(' ')
        if len(text) > 1:
            text_on_buttons = text[1]
        second = int(text[0][:text[0].find('x')])
        first = int(text[0][text[0].find('x')+1:])
    except:
        first = 8
        second = 1
    buttons = [
        [{'text': text_on_buttons, 'callbackData': "nothing"}]*first]*second


    return "Small buttons", buttons


class CollbackLogic:

    def get_answer_by_callback(self, event):
        callback = event.data['callbackData']
        alert = False
        url = ''
        text = ''
        message = f'{callback} pressed.'
        markup = []

        if 'alert' in callback:
            alert = True
        if 'url' in callback:
            url = 'https://mail.ru'
        if 'toast' in callback:
            text = "Toast"
        if 'edit' in callback:
            text = "Отредактировано!"+str(time.time())
            markup = [[{'text': "Отредачено!", 'callbackData': "nothing"}]]
            return {'alert': alert, 'text': text, 'url': url,
            'markup': markup, 'message': message, 'edit':True}

        if 'all' in callback:
            return all(callback)
        if callback in globals():
            if type(globals()[callback]) == tuple:
                if type(globals()[callback][1]) == list:
                    markup = globals()[callback][1]
                    text = globals()[callback][0]
            elif type(globals()[callback]) == str:
                message = globals()[callback]
            else:
                return globals()[callback]()
        if '8x1' in callback:
            text, markup = custom(text)

        return {'alert': alert, 'text': text, 'url': url, 'markup': markup,
         'message': message}

    def get_answer_by_text(self, text):

        answer = 'Привет!'
        markup = default_markup

        if 'x' in text:
            answer, markup = custom(text)
        return {'text': answer, 'markup': markup}
