from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from app.db.models import Base


class RuleHistoryValue(Base):
    __tablename__ = 'rule_history_value'

    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('rule_history.id'), nullable=False)

    content = Column(String, nullable=False)
    groups = Column(String, nullable=True)
    is_new = Column(Boolean, nullable=False, default=False)
