from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema
from app.db import get_db
from app.db.models import Setting
from app.dependencies.security import get_current_user_id

router = APIRouter()


@router.get("/")
def get_settings(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    settings = db.query(Setting).filter_by(user_id=current_user_id).all()
    setting_schema = schema.Setting()
    for setting in settings:
        setattr(setting_schema, setting.key, setting.value)
    return setting_schema


@router.post('/')
def update_settings(params: schema.Setting, db: Session = Depends(get_db),
                    current_user_id: int = Depends(get_current_user_id)):
    pass
