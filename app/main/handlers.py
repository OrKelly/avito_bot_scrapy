from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.main.keyboard import get_main_keyboard, get_admin_keyboard, get_main_keyboard_unsubsribed
from app.users.dao import UsersDAO

router = Router()


@router.message(Command('start'))
async def startup(message: Message):
    user = await UsersDAO.get_one_or_none(user_id=message.from_user.id)
    if not user:
        await UsersDAO.add(user_name=message.from_user.full_name, user_id=message.from_user.id,
                           is_active_subscription=False)
        user = await UsersDAO.get_one_or_none(user_id=message.from_user.id)
    if user.is_admin:
        await message.answer('Привет, Босс! Давайте работать?', reply_markup=get_admin_keyboard())
    elif user.is_active_subscription:
        await message.answer('Привет! Вы уже готовы начать работу со мной? Тогда жмите эти кнопки поскорее!',
                             reply_markup=get_main_keyboard())
    else:
        await message.answer('К сожалению, у вас нет доступа! Узнайте подробную информацию по кнопке "Подписка"',
                             reply_markup=get_main_keyboard_unsubsribed())


@router.callback_query(F.data == 'help_main')
async def send_help_info(callback: CallbackQuery):
    # TODO подумать об HTML шаблоне
    help_text = ("Привет! Меня зовут Скрэпи, и я умею парсить авито. Я уверен, мы подружимся! А теперь коротко о "
                 "том, что я умею:\n\n- я умею парсить страницы авито по вашему запросу. Все просто, вы мне "
                 "присылаете ссылку,а я просматриваю все объявления и присылаю вам документ (xlsx таблицу) "
                 "со всеми объявлениями на странице. Удобно, не правда ли?\n\n - вы можете задать мне ссылки, "
                 "объявления откуда вы хотите получать регулярно. Я буду проверять их раз в сутки и если будет что-то "
                 "новенькое или что-то поменяется в уже существующих - буду сообщать вам об этом!\n\n "
                 "Интересно? Но я работаю только с теми, кто оплачивает мою подписку. Для её оплаты обращайтесь к "
                 "создателю - @OKernior К нему же вы можете обратиться, если у вас возникнут пожелания или проблемы!")
    await callback.message.answer(help_text)


@router.callback_query(F.data == 'sub_help')
async def send_sub_info(callback: CallbackQuery):
    help_text = ("Я работаю только по подписке. Что даст моя подписка:\n\n - Возможность оперативного считывания "
                 "содержимого страницы авито. Теперь вам не придется часами рассматривать объявления, я подаю "
                 "информацию в сжатом и понятном виде!\n\n"
                 "- Если вам важно получать информацию о новых объявлениях в короткие сроки - это тоже ко мне! Вы мо"
                 "жете задать мне ссылки, которые я буду смотреть и присылать вам информацию о новых объявлениях! Must "
                 "have для риелторов.\n\n"
                 "Круто же, согласитесь? Скорее, пишите моему создателю @OKernior, и договоритесь с ним о подписке."
                 "К сожалению, пока что нет возможности внедрить автоматическую подписку, но если мной будут "
                 "пользоваться много людей - это не заставит себя долго ждать.")
    await callback.message.answer(help_text)