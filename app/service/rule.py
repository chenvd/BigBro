from sqlalchemy.orm import Session

from app import schema
from app.db.models import Rule, RuleNotify
from app.db.transaction import transaction
from app.scheduler import scheduler
from app.service import crawler


class RuleService:
    @staticmethod
    def get_rules_by_user(db: Session, user_id: int):
        return db.query(Rule).filter_by(user_id=user_id).all()

    @staticmethod
    @transaction
    def add_rule(db: Session, params: schema.RuleCreate):
        params.favicon = crawler.favicon(params.url)
        rule = Rule(**params.model_dump(exclude={'notify_ids'}))

        rule = rule.add(db)

        for notify_id in params.notify_ids:
            RuleNotify(rule_id=rule.id, notify_id=notify_id).add(db)

        if params.status:
            scheduler.add(rule.id, params.cron)
        return rule.id

    @staticmethod
    @transaction
    def update_rule(db: Session, params: schema.RuleUpdate):
        rule = Rule.get(db, params.id)
        RuleNotify.delete_by_rule(db, rule.id)
        if rule.url != params.url:
            params.favicon = crawler.favicon(params.url)
        rule = rule.update(db, params.model_dump(exclude={'notify_ids'}))
        for notify_id in params.notify_ids:
            RuleNotify(rule_id=rule.id, notify_id=notify_id).add(db)

        if params.status:
            scheduler.add(params.id, params.cron)
        else:
            scheduler.remove(params.id)
