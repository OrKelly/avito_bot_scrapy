from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from .core import config

DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)
