from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema
from app.db import get_db
from app.db.models.notify import Notify
from app.dependencies.security import get_current_user_id
from app.exception import AccessDeniedException
from app.schema.r import R

router = APIRouter()


@router.get("/", response_model=R[List[schema.Notify]])
def get_notifies(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    notifies = db.query(Notify).filter_by(user_id=user_id).all()
    return R.list(notifies)


@router.post("/")
def add_notify(params: schema.NotifyCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    notify = Notify(**params.model_dump())
    notify.user_id = user_id
    notify.add(db)
    return R.ok()


@router.put("/")
def update_notify(params: schema.Notify, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    notify = Notify.get(db, params.id)
    if notify.user_id != user_id:
        raise AccessDeniedException()
    notify.update(db, params.model_dump())
    return R.ok()
