from sqlalchemy import Column, String, Integer, Boolean, BigInteger

from app.settings.db import Base


class User(Base):
    __tablename__ = 'users'

    user_name = Column(String, nullable=True)
    user_id = Column(BigInteger, nullable=False)
    is_active_subscription = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __str__(self):
        return f'User {self.user_name} with id: {self.user_id}'
