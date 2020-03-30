import requests
import logging
import time
import json
from params import *

TOKEN = ''#your token here

base_url = "https://rapi.icq.net/botapi"
get_event_url = f"{base_url}/events/get"
send_message_url = f"{base_url}/messages/sendText"
callback_answer_url = f"{base_url}/messages/answerCallbackQuery"
edit_message_url = f"{base_url}/messages/editText"


def poll(event_id):

    params = {'lastEventId': str(event_id), 'pollTime': 300, 'token': TOKEN}

    reply = requests.get(get_event_url, params)

    if reply.status_code != requests.codes.ok:
        return None

    json = None
    try:
        json = reply.json()
    except Exception as e:
        logging.error('Invalid JSON from server: {}'.format(e))
        logging.error(reply.content)
        return None
    return json

def new_message_event_handler(event):
    chat_id = event['payload']['chat']['chatId']
    logging.debug(event)
    msg_id = event['payload']['msgId']
    text = event['payload']['text'].lower()


    params = get_answer(text)
    if type(params) == list:
        for param in params:
            param.update({'chatId': chat_id, 'token': TOKEN})

            reply = requests.get(send_message_url, param)
            print(reply.text)
    else:
        params.update({'chatId': chat_id, 'token': TOKEN})

        reply = requests.get(send_message_url, params)
        print(reply.text)

def callback_query_event_handler(event):
    try:
        message, params,edit,func = get_callback(event)
    except TypeError as e:
        return 0
    if edit:

        params = {'chatId':event['payload']['message']['chat']['chatId'],'msgId':event['payload']['message']['msgId'],'text':"Отредактировано!"+str(time.time()),'inlineKeyboardMarkup':json.dumps([[{"text": "Отредачено!", "callbackData": "red"}]]),'token': TOKEN}
        r = requests.post(edit_message_url, params)
        print(r.text)
        print("POST "+r.url+', with params: ',params)
        return 0
    if func:
        params_of_func = get_answer(func)
        if type(params_of_func) == list:
            for param in params_of_func:
                param.update({'chatId': event['payload']['message']['chat']['chatId'], 'token': TOKEN})

                reply = requests.get(send_message_url, param)
                print(reply.text)
        else:
            params_of_func.update({'chatId': event['payload']['message']['chat']['chatId'], 'token': TOKEN})

            reply = requests.get(send_message_url, params_of_func)
            print(reply.text)

    params_for_message = {'chatId':event['payload']['message']['chat']['chatId'], 'text':message,'token':TOKEN}
    reply = requests.get(send_message_url, params_for_message)
    print('----------')
    logging.info(event)
    logging.info(params_for_message)
    logging.info(reply.url)
    logging.info(reply.text)
    print('----------')

    params.update({'token': TOKEN})
    r = requests.post(callback_answer_url, params)
    return r.status_code


def event_handler(event):
    logging.info(event)
    try:
        if event['type'] == "newMessage":
            new_message_event_handler(event)
        elif event['type'] == "callbackQuery":
            callback_query_event_handler(event)
    except:
        pass

    return event['eventId']

def run():
    max_event_id = 0
    try:
        while (True):

                json = poll(max_event_id)

                if json is None:
                    continue

                if 'events' not in json:
                    logging.error('No events in JSON: {}'.format(json))
                    continue

                for event in json['events']:
                    max_event_id = max(max_event_id, event_handler(event))
    except:
        pass

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y.%m.%d %I:%M:%S %p',
                        level=logging.DEBUG)

    run()
