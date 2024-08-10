from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.converter.xlsx_converter import ImportXlsx
from app.parser.callback_factory import UrlsCallbackFactory
from app.parser.dao import UserParsingRequestDAO
from app.parser.keyboard import get_parsing_keyboard
from app.parser.parser import Parser
from app.parser.selenium import Selenium
from app.parser.states import ParsingStates
from app.parser.utils import clear_user_media_root

router = Router()


@router.callback_query(F.data == 'parsing_main')
async def parsing_main_handler(callback: types.CallbackQuery):
    await callback.message.answer('Выберите опцию:', reply_markup=get_parsing_keyboard())


@router.callback_query(F.data == 'start_parsing')
async def start_parsing_handler(callback: types.CallbackQuery, state: FSMContext):
    text = ("Пришлите мне ссылку для парсинга. ВАЖНО!\n\nСсылка должна быть с avito.com, вести на отфильтрованную по "
            "вашему запросу страницу (например на страницу квартир в вашем городе). Обязательно указывайте все нужные "
            "вам фильтры (например квартиры только от собственника и тд) перед отправкой ссылки")
    await callback.message.answer(text)
    await state.set_state(ParsingStates.sended_url_for_parse)


@router.message(ParsingStates.sended_url_for_parse)
async def parsing_user_url(message: types.Message, state: FSMContext):
    Selenium(url=message.text, user=message.from_user.id).get_page_source_code()
    parser = Parser(user=message.from_user.id)
    pages_count = await parser.get_pages_count()
    all_ads = []
    for i in range(1, pages_count):
        if i != 1:
            Selenium(url=f'{message.text}&p={i}', user=message.from_user.id, page=i).get_page_source_code()
        parser.page = i
        parsed_page = await parser.parse_page()
        all_ads.extend(parsed_page)
        # for item in parsed_page:
        #     item_data = '\n'.join([f'{key}: {value}' for key, value in item.items()])
        #     await message.answer(item_data)
    clear_user_media_root(user_id=message.from_user.id)
    report = ImportXlsx(data=all_ads, user=message.from_user.id)
    report.create_report()
    file = FSInputFile(report.report_path)
    await message.answer('Готово! Высылаю вам файл')
    await message.answer_document(file)


@router.callback_query(F.data == 'add_parsing_url')
async def add_new_url(callback: types.CallbackQuery, state: FSMContext):
    text = ("Пришлите мне ссылку для парсинга. ВАЖНО!\n\nСсылка должна быть с avito.com, вести на отфильтрованную по "
            "вашему запросу страницу (например на страницу квартир в вашем городе).\n\n Обязательно указывайте все "
            "нужные вам фильтры (например квартиры только от собственника и тд) перед отправкой ссылки")
    await callback.message.answer(text)
    await state.set_state(ParsingStates.sended_url_for_task)


@router.message(ParsingStates.sended_url_for_task)
async def add_user_url_to_parse(message: types.Message, state: FSMContext):
    url = await UserParsingRequestDAO.get_one_or_none(user_id=message.from_user.id, url=message.text)
    if url:
        await message.answer('Вы уже добавляли точно такую ссылку! Вставьте другую!')
    else:
        await UserParsingRequestDAO.add(user_id=message.from_user.id, url=message.text)
        await message.answer('Ссылка успешно добавлена!')


@router.callback_query(F.data == 'parsing_urls')
async def get_parsing_urls(callback: types.CallbackQuery):
    result = await UserParsingRequestDAO.get_user_urls(user_id=callback.from_user.id)
    if result:
        urls = '\n\n'.join(result)
        await callback.message.answer(f'Вот ваши ссылки:\n\n{urls}')
    else:
        await callback.message.answer('Вы еще не добавили ссылки! Время это исправить?')


@router.callback_query(F.data == 'delete_url')
async def show_users_urls_to_delete(callback: types.CallbackQuery):
    urls = await UserParsingRequestDAO.get_user_urls_with_ids(user_id=callback.from_user.id)
    builder = InlineKeyboardBuilder()
    for url in urls:
        builder.button(text=url.url, callback_data=UrlsCallbackFactory(id=url.id))
    builder.adjust(1)
    await callback.message.answer('Выберите ссылку для удаления:', reply_markup=builder.as_markup())


@router.callback_query(UrlsCallbackFactory.filter())
async def delete_url(callback: types.CallbackQuery, callback_data: UrlsCallbackFactory):
    await UserParsingRequestDAO.delete(instance_id=callback_data.id)
    await callback.message.answer('Готово! Ссылка была удалена!')
