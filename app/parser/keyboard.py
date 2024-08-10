from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_parsing_keyboard():
    buttons = [
        [InlineKeyboardButton(text='Запустить парсинг', callback_data='start_parsing')],
        [InlineKeyboardButton(text='Добавить новую ссылку для парсинга', callback_data='add_parsing_url')],
        [InlineKeyboardButton(text='Ссылки для парсинга', callback_data='parsing_urls')],
        [InlineKeyboardButton(text='Удалить ссылку', callback_data='delete_url')]
    ]
    markup = InlineKeyboardMarkup(max_width=1, inline_keyboard=buttons)
    return markup







































































