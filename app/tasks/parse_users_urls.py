import asyncio
import os
import shutil

from aiogram import Bot

from app.parser.dao import UserParsingRequestDAO, ParsingResultDAO
from app.parser.parser import Parser
from app.parser.selenium import Selenium
from app.parser.utils import clear_user_media_root
from app.settings.core import config


class ParseUsersUrlTask:

    def __init__(self, bot):
        self._bot = bot

    @staticmethod
    async def get_urls():
        urls = await UserParsingRequestDAO.get_all()
        return urls

    @staticmethod
    def get_orm_attr_name(attr):
        attrs = {
            'Наименование': 'name',
            'Цена': 'price',
            'Ссылка': 'link',
            'Адрес': 'address'
        }
        return attrs.get(attr, None)

    @staticmethod
    def get_joined_ad(ad):
        if isinstance(ad, dict):
            return '\n\n'.join([f'{key}: {value}' for key, value in ad.items()])
        return '\n\n'.join(ad)

    async def parse_urls(self):
        print('start parse')
        urls = await self.get_urls()
        for url in urls:
            Selenium(url=url.url, user=url.user_id).get_page_source_code()
            parser = Parser(user=url.user_id)
            pages_count = await parser.get_pages_count()
            for i in range(1, 2):
                if i != 1:
                    Selenium(url=f'{url}&p={i}&s=104', user=url.user_id,
                             page=i).get_page_source_code()
                parser.page = i
                parsed_page = await parser.parse_page()
                await self.check_ads(ads=parsed_page, user=url.user_id)
            clear_user_media_root(user_id=url.user_id)

    async def check_ads(self, ads, user):
        for ad in ads:
            existing_ad = await ParsingResultDAO.get_one_or_none(name=ad['Наименование'], address=ad['Адрес'])
            if existing_ad:
                await self.compare_ads(old_ad=existing_ad, new_ad=ad, user=user)
            else:
                ad_text = self.get_joined_ad(ad)
                await self._bot.send_message(user, f'Новое объявление:\n\n{ad_text}')
                await ParsingResultDAO.add(name=ad['Наименование'], address=ad['Адрес'], link=ad['Ссылка'],
                                           price=ad['Цена'], user_id=user)
                await asyncio.sleep(10)

    async def compare_ads(self, old_ad, new_ad, user):
        for key, value in new_ad.items():
            attr = self.get_orm_attr_name(key)
            if attr in old_ad.keys():
                if old_ad[attr] != value:
                    ad_text = self.get_joined_ad(new_ad)
                    await self._bot.send_message(user, f'Обновилось объявление:\n\n{ad_text}')
                    await ParsingResultDAO.update(instance_id=old_ad.id, name=new_ad['Наименование'],
                                                  address=new_ad['Адрес'],
                                                  link=new_ad['Ссылка'], price=new_ad['Цена'])
                    break
