from aiogram.fsm.state import StatesGroup, State


class ParsingStates(StatesGroup):
    sended_url_for_parse = State()
    sended_url_for_task = State()
