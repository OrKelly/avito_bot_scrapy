import os
import sys
from os.path import dirname, abspath
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SOURCES_PAGES_ROOT(self):
        return os.path.join(Path(__file__).resolve().parent.parent, 'source_pages')

    @property
    def MEDIA_ROOT(self):
        return os.path.join(Path(__file__).resolve().parent.parent, 'media')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
