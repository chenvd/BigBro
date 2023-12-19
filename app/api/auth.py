from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models.user import User
from app.exception.biz import BizException
from app.schema.r import R

router = APIRouter()


@router.post("/login")
def get_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    token = User.verify(db, form_data.username, form_data.password)
    if not token:
        raise BizException(message="用户名或密码不正确")
    return R.ok(token)
