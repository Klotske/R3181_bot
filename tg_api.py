from telegram import ReplyKeyboardMarkup

# Место для разметки пользовательских меню

menuMain = ReplyKeyboardMarkup(
    [
        ["Актуальное"],
        ["Мои задания", "Настройки"],
        ["Полезные материалы"]
    ],
    one_time_keyboard=False,
    resize_keyboard=True
)

menuLogin = ReplyKeyboardMarkup(
    [
        ["Студент"],
        ["Гость"]
    ],
    one_time_keyboard=False,
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    [
        ["Назад"]
    ],
    one_time_keyboard=False,
    resize_keyboard=True
)