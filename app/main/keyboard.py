from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard_unsubsribed():
    buttons = [
        [InlineKeyboardButton(text='Получить доступ', callback_data='sub_help')],
        [InlineKeyboardButton(text='F.A.Q.', callback_data='help_main')],
    ]
    markup = InlineKeyboardMarkup(max_width=1, inline_keyboard=buttons)
    return markup


def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text='Парсинг', callback_data='parsing_main')],
        [InlineKeyboardButton(text='F.A.Q.', callback_data='help_parsing')],
    ]
    markup = InlineKeyboardMarkup(max_width=1, inline_keyboard=buttons)
    return markup


def get_admin_keyboard():
    buttons = [
        [InlineKeyboardButton(text='Парсинг', callback_data='parsing_main')],
        [InlineKeyboardButton(text='Выдать доступ', callback_data='give_subscrib')],
        [InlineKeyboardButton(text='Забрать доступ', callback_data='unsubscrib_user')],
        [InlineKeyboardButton(text='Рассылка', callback_data='notificate_users')]
    ]
    markup = InlineKeyboardMarkup(max_width=1, inline_keyboard=buttons)
    return markup
