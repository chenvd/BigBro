from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema
from app.db import get_db
from app.db.models import Rule, RuleHistory
from app.dependencies.security import get_current_user_id
from app.scheduler import scheduler
from app.schema.r import R
from app.service.rule import RuleService

router = APIRouter()


@router.get("/", response_model=R[List[schema.Rule]])
def get_rules(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    rules = RuleService.get_rules_by_user(db, current_user_id)

    rule_schemas = []
    for rule in rules:
        rule_schema = schema.Rule.model_validate(rule)
        rule_schema.notify_ids = [i.id for i in rule.notifies]
        rule_schemas.append(rule_schema)

    return R.list(rule_schemas)


@router.post("/")
def add_rule(params: schema.RuleCreate, db: Session = Depends(get_db),
             current_user_id: int = Depends(get_current_user_id)):
    params.user_id = current_user_id
    rule_id = RuleService.add_rule(db, params)
    scheduler.manually(rule_id)
    return R.ok()


@router.put("/")
def update_rule(params: schema.RuleUpdate, db: Session = Depends(get_db)):
    RuleService.update_rule(db, params)
    scheduler.manually(params.id)
    return R.ok()


@router.post('/trigger')
def trigger_rule(rule_id: int):
    scheduler.manually(rule_id)
    return R.ok()


@router.get('/history', response_model=R[List[schema.RuleHistory]])
def get_rule_history(rule_id: int, only_update: bool, db: Session = Depends(get_db)):
    histories = db.query(RuleHistory).filter_by(rule_id=rule_id)
    if only_update:
        histories = histories.filter_by(status=1)
    histories = histories.order_by(RuleHistory.id.desc()).all()

    rule = Rule.get(db, rule_id)
    if rule.has_new:
        rule.update(db, {'has_new': False})
    return R.ok(data=histories)
