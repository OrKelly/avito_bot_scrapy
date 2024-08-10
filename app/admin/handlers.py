from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.admin.states import AdminStates

from app.parser.dao import UserParsingRequestDAO, ParsingResultDAO
from app.settings.core import config
from app.users.dao import UsersDAO

router = Router()
bot = Bot(config.TOKEN)


@router.callback_query(F.data == 'give_subscrib')
async def await_user_id_to_sub(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите айди пользователя для выдачи доступа')
    await state.set_state(AdminStates.sended_user_id_to_sub)


@router.message(AdminStates.sended_user_id_to_sub)
async def give_sub_for_user(message: Message):
    user_id = int(message.text)
    user = await UsersDAO.get_one_or_none(user_id=user_id)
    if not user:
        await message.answer('Указанный пользователь не найден!')
    else:
        await UsersDAO.update(instance_id=user.id, is_active_subscription=True)
        await message.answer(f'Пользователю {user_id} был выдан доступ!')


@router.callback_query(F.data == 'notificate_users')
async def await_message_for_notificate_users(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите текст для рассылки')
    await state.set_state(AdminStates.sended_message_for_notificate)


@router.message(AdminStates.sended_message_for_notificate)
async def start_notificate_users(message: Message):
    users = await UsersDAO.get_all()
    await message.answer('Рассылка успешно начата!')
    for user in users:
        await bot.send_message(chat_id=user.user_id, text=message.text)


@router.callback_query(F.data == 'unsubscrib_user')
async def await_user_id_to_unscrib(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите айди пользователя для отвязки')
    await state.set_state(AdminStates.sended_user_id_to_unsub)


@router.message(AdminStates.sended_user_id_to_unsub)
async def unsub_user(message: Message):
    user_id = int(message.text)
    user = await UsersDAO.get_one_or_none(user_id=user_id)
    if not user:
        await message.answer('Указанный пользователь не найден!')
    else:
        await UserParsingRequestDAO.delete(user_id=user_id)
        await ParsingResultDAO.delete(user_id=user_id)
        await UsersDAO.update(instance_id=user.id, is_active_subscription=False)
        await message.answer(f'У пользователя {user_id} была отменена подписка! Все его запросы были очищены')
