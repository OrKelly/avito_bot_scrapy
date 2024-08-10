from aiogram.filters.callback_data import CallbackData


class UrlsCallbackFactory(CallbackData, prefix="faburls"):
    id: int
