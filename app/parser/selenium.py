import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from app.parser.proxy import Proxy
from app.settings.core import config


class Selenium:
    ROOT = config.SOURCES_PAGES_ROOT

    def __init__(self, url, user, page=1, settings: dict = None):
        self.url = url
        self._headers = self.headers
        self.user = user
        self.page = page
        self._options = self.set_options(settings)

    @property
    def headers(self):
        return {'authority': 'm.avito.ru',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                          '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'ru-RU,ru;q=0.9', }

    def set_options(self, settings: dict) -> Options:
        options = webdriver.FirefoxOptions()
        if settings:
            for option, value in settings.items():
                options.add_argument(f'{option}={value}')
        options.add_argument('--headless=new')
        return options

    def get_proxy_url(self):
        proxy = Proxy().get_proxy_url()
        return proxy
    def check_or_create_sources_root(self):
        source_root = os.path.join(self.ROOT, str(self.user))
        if not os.path.exists(source_root):
            os.mkdir(source_root)

    def get_page_source_code(self):
        self.check_or_create_sources_root()
        self._options.add_argument(f'--proxy-server={self.get_proxy_url()}')
        driver = webdriver.Firefox(options=self._options)
        driver.maximize_window()
        try:
            driver.get(url=self.url)
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.TAG_NAME, "html")))
            if 'Доступ ограничен' in driver.page_source:
                sleep(60)
                print('Retry')
                self.get_page_source_code()
            with open(f'{self.ROOT}/{self.user}/page_{self.page}_source-page.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)
        except Exception as ex:
            print(ex)
            sleep(10)
            self.get_page_source_code()
        finally:
            driver.close()
            driver.quit()
