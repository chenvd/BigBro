from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import Session

from app.db.models.base import Base
from app.db.transaction import transaction


class RuleNotify(Base):
    __tablename__ = "rule_notify"

    rule_id = Column(Integer, ForeignKey("rule.id"), primary_key=True, nullable=False)
    notify_id = Column(Integer, ForeignKey("notify.id"), primary_key=True, nullable=False)

    @classmethod
    @transaction
    def delete_by_rule(cls, db: Session, rule_id: int):
        db.query(cls).filter_by(rule_id=rule_id).delete()
