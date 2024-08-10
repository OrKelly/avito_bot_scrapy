from sqlalchemy import select

from app.dao.dao import BaseDAO
from app.parser.models import UserParsingRequest, ParsingResult
from app.settings.db import async_session_maker


class UserParsingRequestDAO(BaseDAO):
    model = UserParsingRequest

    @classmethod
    async def get_user_urls(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.c.url).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_user_urls_with_ids(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.c.id, cls.model.__table__.c.url).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()


class ParsingResultDAO(BaseDAO):
    model = ParsingResult
