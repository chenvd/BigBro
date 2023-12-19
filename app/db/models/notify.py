from sqlalchemy import Column, Integer, ForeignKey, String, Enum

from app.db.models.base import Base


class Notify(Base):
    __tablename__ = 'notify'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(
        'telegram', 'webhook'
    ), nullable=False)
    payload = Column(String, nullable=False)
