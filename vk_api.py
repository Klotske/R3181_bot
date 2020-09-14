import vk
import json, time
import settings

session = vk.Session()
api = vk.API(session, v=5.122)


def sendMessage(user_id, message, keyboard="",  token=settings.token, attachment=""):
    random_id = int(time.time() * 10000)
    api.messages.send(access_token=token, user_id=str(
        user_id), random_id=random_id, message=str(message), keyboard=keyboard, attachment=attachment)


def getUserName(user_id, token=settings.token):
    info = api.users.get(access_token=token,
                         user_ids=user_id, name_case='Nom')[0]
    name = info['first_name'] + " " + info['last_name']
    return name

def getButton(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

def getKeyboard(keyboard):
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    return str(keyboard.decode('utf-8'))

# Место для разметки пользовательских меню

menuMain = getKeyboard(
    {
        "one_time": False,
        "buttons": [
            [getButton("Актуальное", "positive")],
            [getButton("Мои задания", "primary"), getButton("Настройки", "primary")],
            [getButton("Полезные материалы", "primary")]
        ]
    }
)

menuLogin = getKeyboard(
    {
        "one_time": False,
        "buttons": [
            [getButton("Студент", "positive")],
            [getButton("Гость", "primitive")]
        ]
    }
)

back = getKeyboard(
    {
        "one_time": False,
        "buttons": [
            [getButton("Назад", "negative")]
        ]
    }
)