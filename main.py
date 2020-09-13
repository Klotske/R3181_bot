from flask import Flask, request, json
import json as js
import sys
import telegram, settings, vk_api, tg_api

app = Flask(__name__)

bot = telegram.Bot(token=settings.tg_token)

@app.route('/')
def main():
    return "Hello World"

@app.route('/vk/', methods=["POST"])
def vk_hook():
    data = json.loads(request.data)
    if "type" not in data.keys():
        return "non_vk"
    elif data['type'] == "confrimation":
        print("VK requested confrimation code")
        return settings.confirmationCode
    elif data['type'] == "message_new":
        user_id = data['object']['message']['from_id']
        try:
            text = data['object']['message']['text']
            msg = text.lower()
            print("(VK) ID пользователя: ", user_id, "Сообщение: ", text)
            if msg == "привет":
                vk_api.sendMessage(user_id, "Привет!")
        except (KeyError, TypeError) as e:
            print("(VK) Error: ", e, sys.exc_info()[0], sys.exc_info()[1])

@app.route('/tg/', methods=["POST"])
def tg_hook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    try:
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        text = update.message.text.encode("utf-8").decode()
        msg = text.lower()
        print("(TG) ID пользователя", user_id, "Сообщение: ", text)
        if msg in ['/start', 'привет']:
            bot.sendMessage(chat_id, "Привет")
    except (KeyError, TypeError) as e:
        print("(TG) Error: ", e, sys.exc_info()[0], sys.exc_info()[1])