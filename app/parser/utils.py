import os
import shutil
from typing import Union

from app.settings.core import config


def clear_user_media_root(user_id: Union[int, str]):
    """Функция удаляет папку со спарсенными html страницами"""
    user_root = os.path.join(config.SOURCES_PAGES_ROOT, str(user_id))
    shutil.rmtree(user_root)

