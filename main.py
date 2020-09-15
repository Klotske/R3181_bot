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
homeDir = '/home/klotskedev/bot/files/'

# Ответы бота
Data = {}

# Пользовательские данные (Текущая позиция в меню)
vkData = {}
tgData = {}

def loadData():
    global Data
    Data = js.load(open(homeDir+"Data.json", 'r', encoding='utf-8'))

def loadVK():
    global vkData
    vkData = js.load(open(homeDir+"vkData.json", 'r', encoding='utf-8'))
    print("(VK) vkData загружена")


def saveVK():
    js.dump(vkData, open(homeDir+"vkData.json", 'w', encoding='utf-8'),
            ensure_ascii=False, indent=4, separators=(',', ': '))


def loadTG():
    global tgData
    tgData = js.load(open(homeDir+"tgData.json", 'r', encoding='utf-8'))
    print("(TG) tgData загружена")


def saveTG():
    js.dump(tgData, open(homeDir+"tgData.json", 'w', encoding='utf-8'),
            ensure_ascii=False, indent=4, separators=(',', ': '))

loadData()
loadVK()
loadTG()

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
                vkData.update({str(user_id): {'step': 'login'}})
                vk_api.sendMessage(user_id, Data['login'], keyboard=vk_api.menuLogin)
            else:
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
                # Главное меню
                elif vkData[str(user_id)]['step'] == 'menu':
                    if msg == 'актуальное':
                        vkData[str(user_id)]['step'] = 'actual'
                        vk_api.sendMessage(str(user_id), "Актуальное", keyboard=vk_api.back)
                    elif msg == 'мои задания':
                        vkData[str(user_id)]['step'] = 'my_tasks'
                        vk_api.sendMessage(str(user_id), "Мои задания", keyboard=vk_api.back)
                    elif msg == 'настройки':
                        vkData[str(user_id)]['step'] = 'settings'
                        vk_api.sendMessage(str(user_id), "Настройки", keyboard=vk_api.back)
                    elif msg == 'полезные материалы':
                        vkData[str(user_id)]['step'] = 'useful_info'
                        vk_api.sendMessage(str(user_id), "Полезные материалы", keyboard=vk_api.back)
                    else:
                        vk_api.sendMessage(str(user_id), Data['err'], keyboard=vk_api.menuMain)
                # Актуальное, Мои задания
                elif vkData[str(user_id)]['step'] in ['actual', 'my_tasks']:
                    if msg == 'назад':
                        vkData[str(user_id)]['step'] = 'menu'
                        vk_api.sendMessage(str(user_id), 'Главное меню', keyboard=vk_api.menuMain)
                # Настройки
                elif vkData[str(user_id)]['step'] == 'settings':
                    if msg == 'назад':
                        vkData[str(user_id)]['step'] = 'menu'
                        vk_api.sendMessage(str(user_id), 'Главное меню', keyboard=vk_api.menuMain)
                # Полезные материалы
                elif vkData[str(user_id)]['step'] == 'useful_info':
                    if msg == 'назад':
                        vkData[str(user_id)]['step'] = 'menu'
                        vk_api.sendMessage(str(user_id), 'Главное меню', keyboard=vk_api.menuMain)

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
        if msg in ['начать', 'start', '/back', '/start']:
            tgData.update({str(user_id): {'step': 'login'}})
            bot.sendMessage(user_id, Data['login'], reply_markup=tg_api.menuLogin)
        else:
            # Логин
            if tgData[str(user_id)]['step'] == 'login':
                if msg == 'студент':
                    tgData[str(user_id)]['step'] = 'login'
                    bot.sendMessage(chat_id, Data['student_login'])
                if msg == 'гость':
                    tgData.update({str(user_id): {'isu': 'guest'}})
                    tgData[str(user_id)]['step'] = 'menu'
                    bot.sendMessage(chat_id, Data['info'], reply_markup=tg_api.menuMain)
                if msg.isdigit():
                    tgData.update({str(user_id): {'isu': str(msg)}})
                    tgData[str(user_id)]['step'] = 'menu'
                    bot.sendMessage(chat_id, Data['info'], reply_markup=tg_api.menuMain)
            # Главное меню
            elif tgData[str(user_id)]['step'] == 'menu':
                if msg == 'актуальное':
                    tgData[str(user_id)]['step'] = 'actual'
                    bot.sendMessage(chat_id, "Актуальное", reply_markup=tg_api.back)
                elif msg == 'мои задания':
                    tgData[str(user_id)]['step'] = 'my_tasks'
                    bot.sendMessage(chat_id, "Мои задания", reply_markup=tg_api.back)
                elif msg == 'настройки':
                    tgData[str(user_id)]['step'] = 'settings'
                    bot.sendMessage(chat_id, "Настройки", reply_markup=tg_api.back)
                elif msg == 'полезные материалы':
                    tgData[str(user_id)]['step'] = 'useful_info'
                    bot.sendMessage(chat_id, "Полезные материалы", reply_markup=tg_api.back)
                else:
                    bot.sendMessage(chat_id, Data['err'], reply_markup=tg_api.menuMain)
            # Актуальное, Мои задания
            elif tgData[str(user_id)]['step'] in ['actual', 'my_tasks']:
                if msg == 'назад':
                    tgData[str(user_id)]['step'] = 'menu'
                    bot.sendMessage(chat_id, 'Главное меню', reply_markup=tg_api.menuMain)
            # Настройки
            elif tgData[str(user_id)]['step'] == 'settings':
                if msg == 'назад':
                    tgData[str(user_id)]['step'] = 'menu'
                    bot.sendMessage(chat_id, 'Главное меню', reply_markup=tg_api.menuMain)
            # Полезные материалы
            elif tgData[str(user_id)]['step'] == 'useful_info':
                if msg == 'назад':
                    tgData[str(user_id)]['step'] = 'menu'
                    bot.sendMessage(chat_id, 'Главное меню', reply_markup=tg_api.menuMain)
        
        saveTG()
        return 'ok'
    except (KeyError, TypeError) as e:
        print("(TG) Error: ", e, sys.exc_info()[0], sys.exc_info()[1])
        return 'ok'
