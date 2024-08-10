from sqlalchemy import Column, String, ForeignKey, Boolean, JSON, BigInteger

from app.settings.db import Base


class UserParsingRequest(Base):
    __tablename__ = 'user_parsing_request'

    url = Column(String, nullable=False)
    user_id = Column(BigInteger, nullable=False)


class ParsingResult(Base):
    __tablename__ = 'parsing_result'

    name = Column(String, nullable=False)
    price = Column(String, nullable=True)
    link = Column(String, nullable=True)
    address = Column(String, nullable=True)
    user_id = Column(BigInteger, nullable=False)
