from flask import Flask, request, json
import json as js
import sys
import telegram
import settings
import vk_api
import tg_api

app = Flask(__name__)

bot = telegram.Bot(token=settings.tg_token)

# Рабочая директория
homeDir = '/home/***/bot/'

# Ответы бота
Data = {}

# Пользовательские данные (Текущая позиция в меню)
vkData = {}
tgData = {}

def loadData():
    global Data
    Data = js.load(open(homeDir.join("Data.json"), 'r', encoding='utf-8'))

def loadVK():
    global vkData
    vkData = js.load(open(homeDir.join("vkData.json"), 'r', encoding='utf-8'))
    print("(VK) vkData загружена")


def saveVK():
    js.dump(vkData, open(homeDir.join("vkData.json"), 'w', encoding='utf-8'),
            ensure_ascii=False, indent=4, separators=(',', ': '))


def loadTG():
    global tgData
    tgData = js.load(open(homeDir.join("tgData.json"), 'r', encoding='utf-8'))
    print("(TG) tgData загружена")


def saveTG():
    js.dump(tgData, open(homeDir.join("tgData.json"), 'w', encoding='utf-8'),
            ensure_ascii=False, indent=4, separators=(',', ': '))

loadData()

@app.route('/')
def main():
    return "Hello World"


@app.route('/vk/', methods=["POST"])
def vk_hook():
    data = json.loads(request.data)
    if "type" not in data.keys():
        return "non_vk"
    elif data['type'] == "confirmation":
        print("(VK) requested confirmation code")
        return settings.confirmationCode
    elif data['type'] == "message_new":
        user_id = data['object']['message']['from_id']
        try:
            text = data['object']['message']['text']
            msg = text.lower()
            print("(VK) ID пользователя: ", user_id, "Сообщение: ", text)
            
            if msg in ['начать', 'start', '/back', '/start']:
                if str(user_id) in vkData.keys():
                    vkData[str(user_id)]['step'] = 'menu'
                    vk_api.sendMessage(user_id, Data['greeting'], keyboard=vk_api.menuMain)
                else:
                    vkData.update({str(user_id): {'step': 'login'}})
                    vk_api.sendMessage(user_id, Data['login'], keyboard=vk_api.menuLogin)
            else:
                # Главное меню
                if vkData[str(user_id)]['step'] == 'menu':
                    if msg == 'актуальное':
                        vk_api.sendMessage(str(user_id), Data['wip'], keyboard=vk_api.back)
                    elif msg == 'мои задания':
                        vk_api.sendMessage(str(user_id), Data['wip'], keyboard=vk_api.back)
                    elif msg == 'настройки':
                        vk_api.sendMessage(str(user_id), Data['wip'], keyboard=vk_api.back)
                    elif msg == 'полезные материалы':
                        vk_api.sendMessage(str(user_id), Data['wip'], keyboard=vk_api.back)
                    else:
                        vk_api.sendMessage(str(user_id), Data['err'], keyboard=vk_api.menuMain)
                # Логин
                if vkData[str(user_id)]['step'] == 'login':
                    if msg == 'студент':
                        vkData[str(user_id)]['step'] = 'login'
                        vk_api.sendMessage(str(user_id), Data['student_login'])
                    if msg == 'гость':
                        vkData.update({str(user_id): {'isu': 'guest'}})
                        vkData[str(user_id)]['step'] = 'menu'
                        vk_api.sendMessage(str(user_id), Data['info'], keyboard=vk_api.menuMain)
                    if msg.isdigit():
                        vkData.update({str(user_id): {'isu': str(msg)}})
                        vkData[str(user_id)]['step'] = 'menu'
                        vk_api.sendMessage(str(user_id), Data['info'], keyboard=vk_api.menuMain)
            saveVK()
            return 'ok'
        except:
            print("(VK) Error: ", sys.exc_info()[0], sys.exc_info()[1])
            return 'ok'


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
        return 'ok'
    except (KeyError, TypeError) as e:
        print("(TG) Error: ", e, sys.exc_info()[0], sys.exc_info()[1])
        return 'ok'
