from data.import_lib import *
from tools.photo_to_text.languages import language_dict_google


def get_start_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Главное меню🔧', callback_data='main')],
        [InlineKeyboardButton('О боте🤖', callback_data='info')]
    ])

    return ikb


def get_main_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Перевод текста с фото📷', callback_data='scan')],
        [InlineKeyboardButton('Переводчик👄', callback_data='translator')],
        [InlineKeyboardButton('Мой словарь📖', callback_data='user_dict')],
        [InlineKeyboardButton('Назад🔙', callback_data='back')]
    ])

    return ikb


def get_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Вернуться в главное меню🔙', callback_data='main')]
    ])

    return ikb


def get_back() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Назад🔙', callback_data='back')]
    ])

    return ikb


def get_back_ikb_dict() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить слово🆕', callback_data='add_word')],
        [InlineKeyboardButton('Удалить слово🔨', callback_data='del_word')],
        [InlineKeyboardButton('Вернуться в главное меню🔙', callback_data='main')]
    ])

    return ikb


def get_yes_or_no() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('👍', callback_data='yes')],
        [InlineKeyboardButton('👎', callback_data='no')]
    ])

    return ikb


def get_languages() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(lang, callback_data=f'lang_{call}')]
                                                for call, lang in language_dict_google.items()])

    return ikb


def get_dict_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Назад🔙', callback_data='user_dict')]
    ])

    return ikb
