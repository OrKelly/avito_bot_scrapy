import re

import aiofiles
from bs4 import BeautifulSoup
from app.settings.core import config


class Parser:
    def __init__(self, user, page=1):
        self.page = page
        self.user = user

    async def get_page_content(self):
        async with aiofiles.open(f'{config.SOURCES_PAGES_ROOT}/{self.user}'
                                 f'/page_{self.page}_source-page.html', encoding='utf-8') as file:
            result = await file.read()
        return result

    async def parse_page(self):
        result = await self.get_page_content()
        soup = BeautifulSoup(result, 'lxml')
        items = soup.find_all('div', class_=re.compile('iva-item-content'))
        data = []
        for item in items:
            name = item.find('div', class_=re.compile('iva-item-title')).find('h3').get_text(strip=True)
            price = item.find('div', class_=re.compile('iva-item-price')).find('span').find('div').find('strong').find('span').get_text(strip=True)
            address = item.find('div', class_=re.compile('geo-root')).get_text(strip=True)
            date = item.find('div', class_=re.compile('iva-item-date')).find('p').get_text(strip=True)
            link = 'https://www.avito.ru/' + item.find('a').get('href')
            data.append({
                "Наименование": name,
                'Цена': price,
                'Адрес': address,
                'Дата': date,
                'Ссылка': link
            })
        return data

    async def get_pages_count(self):
        result = await self.get_page_content()
        soup = BeautifulSoup(result, 'lxml')
        pages_count = soup.find('div', class_='js-pages pagination-pagination-_FSNE').find_all('li')[-2].text
        return int(pages_count)
