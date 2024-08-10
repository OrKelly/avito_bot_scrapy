from copy import copy

from sqlalchemy import select, insert, delete, update

from app.settings.db import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update(cls, instance_id, **updated_data):
        async with async_session_maker() as session:
            result_data = copy(updated_data)
            for column, data in updated_data.items():
                if data is None:
                    del result_data[column]
            stmt = (update(cls.model).
                    values(**result_data).
                    filter_by(id=instance_id))
            await session.execute(stmt)
            await session.commit()
