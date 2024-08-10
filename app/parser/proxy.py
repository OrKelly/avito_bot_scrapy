import json
from time import sleep

import requests

import aiohttp

from app.settings.core import config


class Proxy:

    def __init__(self, country='RU'):
        self.country = country

    def get_request_body(self):
        request_body = {
            'country': self.country,
            'protocol': 'http',
            'get': 'true',
            'supportsHttps': 'true'
        }
        return request_body

    def get_proxy_url(self):
        request_body = self.get_request_body()
        response = requests.get(f'https://gimmeproxy.com/api/getProxy', params=request_body)
        if response.status_code != 200:
            sleep(20)
            self.get_proxy_url()
        response_json = json.loads(response.content)
        proxy_url = f'http://{response_json["ip"]}:{response_json["port"]}'
        return proxy_url