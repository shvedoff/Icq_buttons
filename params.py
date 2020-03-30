import logging
import requests
import json
import string
from random import randrange, choice, random


all_alerts_types_markup =json.dumps([
        [{"text": "Callback: Nothing", "callbackData": "red"}],
        [{"text": "Callback: Toast", "callbackData": "toast"}],
        [{"text": "Callback: Alert", "callbackData": "alert"}],
        [{"text": "Callback: Url", "callbackData": "url"}],
        [{"text": "Callback: Alert+Url", "callbackData": "alert_url"}],
        [{"text": "Callback: Toast+Url", "callbackData": "toast_url"}],
        [{"text": "Only Url", "url": "http://mail.ru"}],
        [{"text": "Nothing(no callback)","callbackData": "noooo"}],
                                    ])
newline_markup = json.dumps([
        [{"text": "Hello", "callbackData": "red"},
        {"text": "hello\nolleh", "callbackData": "red"},
        {"text": "Привет", "callbackData": "red"}]
                            ])
long_text_on_button_markup = json.dumps(
[[{"text": "Lorem ipsum dolor sit amet, \
consectetur adipiscing elit, sed do eiusmod tempor incididunt ut\
labore et dolore magna aliqua.", "callbackData": "red"}]])

text_on_button_markup = json.dumps([[{"text": "Lorem", "callbackData": "red"}]])

styles = ["primary","attention","base"]

all_styles_markup =json.dumps([
[{"text": "primary style", "callbackData": "red","style":"primary"}],
[{"text": "attention style", "callbackData": "red","style":"attention"}],
[{"text": "base style", "callbackData": "red","style":"base"}],
])

default_reply = {
'text':'Привет!',
'inlineKeyboardMarkup'   :json.dumps([
[{"text": "Все действия с кнопками", "callbackData": "func_all_types"}],
[{"text": "Маленькие кнопки", "callbackData": "func_8x8"}],
[{"text": "Все типы медиа", "callbackData": "func_all_media"}],
[{"text": "Длинный текст в кнопке", "callbackData": "func_all_long"}],
[{"text": "С переносом строки", "callbackData": "func_newline"}],
[{"text": "Своя конфигурация", "callbackData": "func_custom"}],
[{"text": "Сообщение, которое можно отредактировать", "callbackData": "func_edit"}],
[{"text": "Все типы стилей", "callbackData": "func_styles"}],
[{"text": "Рандом...", "callbackData": "func_rand"}],
])
}

types = {
        "text": "текст",
        "long_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "photo": "https://files.icq.net/get/0jmjm00050gDpoit4ZDA2B5e6b480a1ac",
        "photo_2": "https://files.icq.net/get/063c60006MEvtsURDaPvaW5e6b8b951ac",
        "video": "https://files.icq.net/get/8akak0008BfM3IFsSs4qwf5e67861f1bc",
        "gif": "https://media.giphy.com/media/l2R0aKwejYr8ycKAg/giphy.gif",
        "url": "https://www.mail.ru",
        "profile": "https://icq.im/stickers_bot",
        "sticker": "https://files.icq.net/get/28Ialp8YPunsdcuLpIixxk5a2fe49e1af",
        "ptt":"https://files.icq.net/get/I0006DFE9MCGf1vdkUBZCs570bc6701bf"
    }

def get_answer(text):
    reply = default_reply
    print("got text",text)
    if text == 'custom':
        reply = {
        'text':"Напиши текст в формате: AxB text, чтобы получить сетку кнопок размера A на B c тектом text. Пример: 2x3 привет ",
        }
    elif text == 'edit':
        reply = {
        'text':"Жми!",
        'inlineKeyboardMarkup': json.dumps([[{"text": "Жми!", "callbackData": "will_ed"}]])
        }
    elif text == 'styles':
        reply = {
        'text':"Все стили",
        'inlineKeyboardMarkup'   :all_styles_markup
        }
    elif text == 'rand':
        lines_count = randrange(13)+1
        callback = []
        print('lines count',lines_count)
        for i in range(lines_count):

            colls_count = randrange(8)+1
            print('colls_count',colls_count)
            lines = []
            for j in range(colls_count):
                print('ololo',j)
                button = {}
                string_on_button = ''
                for k in range(randrange(5)+1):
                    lower_upper_alphabet = string.ascii_letters
                    string_on_button += choice(lower_upper_alphabet)
                    if random()>0.8:
                        string_on_button+='\n'
                print(string_on_button)
                button["text"] = string_on_button.strip()
                button["callbackData"] = "red"
                button["style"] = choice(styles)
                lines.append(button)
            callback.append(lines)
        callback = json.dumps(callback)
        reply = {
        'text':"Нарандомилось:",
        'inlineKeyboardMarkup'   :callback
        }
        print(reply)

    elif text == 'will_ed':
        reply = {}
        edit = True
    elif text=='newline':
        reply = {
        'text':"Кнопки с переносом строки",
        'inlineKeyboardMarkup'   :newline_markup
        }
    elif text == 'all_long':
        buttons = [[{"text": 'Все', "callbackData": "func_longm_all"}]]
        for key in types.keys():
            buttons.append([{"text": key, "callbackData": "func_longm_"+key}])
        reply = {
        'text':'есть такие c длинным текстом на кнопке:',
        'inlineKeyboardMarkup'   :json.dumps(buttons)
        }
    elif 'longm_' in text:
        type=text[6:]
        print('got long'+text)
        if type == 'all':
            reply = []
            for type in types.keys():
                reply.append(
                {
                'text':types[type],
                'inlineKeyboardMarkup':long_text_on_button_markup
                })
        else:
            reply = {
            'text':types[type],
            'inlineKeyboardMarkup'   :long_text_on_button_markup
            }
    elif text == "all_media":
        buttons = [[{"text": 'Все', "callbackData": "func_media_all"}]]
        for key in types.keys():
            buttons.append([{"text": key, "callbackData": "func_media_"+key}])
        reply = {
        'text':'есть такие:',
        'inlineKeyboardMarkup'   :json.dumps(buttons)
        }
    elif text == "all_types":

        reply = {
        'text':'Все действия с кнопками',
        'inlineKeyboardMarkup'   :all_alerts_types_markup
        }
    elif 'media_' in text:
        type=text[6:]
        print(type)
        print('got media'+text)
        if type == 'all':
            reply = []
            for type in types.keys():
                reply.append(
                {
                'text':types[type],
                'inlineKeyboardMarkup':text_on_button_markup
                })
        else:
            reply = {
            'text':types[type],
            'inlineKeyboardMarkup'   :text_on_button_markup
            }

    elif "x" in text:
        text_on_buttons = 'a'
        try:
            text = text.split(' ')
            print(text)
            if len(text)>1:
                text_on_buttons = text[1]

            print(text[0][:text[0].find('x')],text[0][text[0].find('x'):])
            second = int(text[0][:text[0].find('x')])
            first = int(text[0][text[0].find('x')+1:])
        except:
            first = 8
            second = 1
        line = f'"text":"{text_on_buttons}" , "callbackData": "red"'
        line ='{'+line+'}'
        line = f'{line},'*first
        line = f'[{line[:-1]}],'*second
        line =  f'[{line[:-1]}]'

        print(line)

        reply = {
        'text':'Small buttons',
        'inlineKeyboardMarkup'   :line
        }
    return reply


def get_callback(event):
    data = event['payload']['callbackData']
    alert = "false"
    url = None
    text = ""
    message = ""
    edit = False
    func = False
    try:
        if data != 'noooo':
            message = f'{data} button pressed'


        if data == 'url':
            url = 'https://mail.ru'
        if data == 'toast':
            text = 'Button pressed...'
        if data == 'alert':
            text = 'Button pressed!!!'
            alert = 'true'
        if data == 'alert_url':
            text = "Alert+Url pressed!"
            alert = 'true'
            url = 'https://mail.ru'
        if data == 'toast_url':
            text = "Alert+Url pressed!"
            url = 'https://mail.ru'
        if data == 'will_ed':
            edit = True
        if data == 'noooo':
            return 0
        if 'func' in data:
            func = data[5:]


    except Exception as e:
        logging.warning('button processing exception: {}'.format(e))

    return message, {'queryId': event['payload']['queryId'], 'text': text, 'url': url, 'showAlert': alert}, edit, func
