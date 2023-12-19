from sqlalchemy import Column, String, Integer, ForeignKey

from .base import Base


class Setting(Base):
    __tablename__ = 'setting'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, primary_key=True)
    key = Column(String, nullable=False, primary_key=True)
    value = Column(String, nullable=True)
