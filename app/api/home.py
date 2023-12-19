from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import schema
from app.scheduler import scheduler
from app.db import get_db
from app.db.models import Rule, RuleHistory
from app.dependencies.security import get_current_user_id
from app.schema.r import R

router = APIRouter()


@router.get('/statistic')
def get_statistics(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    rules = db.query(Rule).filter_by(user_id=current_user_id).all()
    today_update = db.query(RuleHistory).filter(
        func.date(RuleHistory.create_time, 'auto') == func.Date(),
        RuleHistory.status == 1,
        RuleHistory.rule_id.in_([i.id for i in rules])
    ).count()

    return R.ok(
        {'rule_count': len(rules), 'today_update': today_update}
    )


@router.get('/schedule', response_model=R[List[schema.HomeSchedule]])
def get_schedule(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    schedules = scheduler.list()
    rules = db.query(Rule).filter(Rule.user_id == current_user_id, Rule.id.in_([i.id for i in schedules])).all()
    results = []
    for rule in rules:
        matched = list(filter(lambda item: item.id == str(rule.id), schedules))
        if matched:
            results.append(schema.HomeSchedule(
                id=rule.id,
                title=rule.name,
                next_time=matched[0].next_run_time,
                favicon=rule.favicon
            ))
    results = sorted(results, key=lambda i: i.next_time)
    return R.list(results)
