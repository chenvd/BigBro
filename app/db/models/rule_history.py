from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Relationship

from app.db.models import Base


class RuleHistory(Base):
    __tablename__ = 'rule_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey('rule.id'), nullable=False)

    status = Column(Integer, nullable=False, default=0, comment="是否有更新")
    content = Column(String, nullable=False)

    values = Relationship('RuleHistoryValue', lazy='joined')
