from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    sended_message_for_notificate = State()
    sended_user_id_to_sub = State()
    sended_user_id_to_unsub = State()