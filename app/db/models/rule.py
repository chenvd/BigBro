from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Relationship, Session

from app import schema
from app.db.models.rule_notify import RuleNotify
from app.db.models.base import Base
from app.db.transaction import transaction


class Rule(Base):
    __tablename__ = 'rule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    favicon = Column(String, nullable=False)

    user_agent = Column(String, nullable=True)
    cookies = Column(String, nullable=True)
    cron = Column(String, nullable=False)

    is_list = Column(Boolean, nullable=False, default=False)
    xpath = Column(String, nullable=True)
    regex = Column(String, nullable=True)

    has_new = Column(Boolean, nullable=False, default=False)
    latest_execute = Column(DateTime, nullable=True)
    latest_update = Column(DateTime, nullable=True)

    status = Column(Boolean, nullable=False, default=True)

    notifies = Relationship('Notify', secondary='rule_notify', lazy='joined')
