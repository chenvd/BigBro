from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema
from app.db import get_db
from app.db.models.user import User
from app.dependencies.security import get_current_user_id, get_current_admin_user, get_current_user
from app.exception import AccessDeniedException, BizException
from app.schema.r import R
from app.utils.security import get_password_hash

router = APIRouter()


@router.get('/', response_model=R[schema.User])
def get_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return R.ok(User.get(db, rid=user_id))


@router.get('/list', response_model=R[List[schema.User]])
def get_user_list(db: Session = Depends(get_db), admin: User = Depends(get_current_admin_user)):
    if admin:
        return R.list(User.list(db))
    else:
        raise AccessDeniedException()


@router.post('/')
def create_user(params: schema.UserCreate, db: Session = Depends(get_db), _=Depends(get_current_admin_user)):
    exist = User.get_by_username(db, params.username)
    if exist:
        raise BizException("该用户名已存在")
    user = User(**params.model_dump())
    user.password = get_password_hash(params.password)
    user.add(db)
    return R.ok()


@router.put('/')
def update_user(params: schema.UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if params.id != user.id and not user.is_admin:
        raise AccessDeniedException()

    exist = User.get_by_username(db, params.username)
    if exist and exist.id != params.id:
        raise BizException("该用户名已存在")
    user = User.get(db, params.id)
    if params.password:
        params.password = get_password_hash(params.password)
    else:
        params.password = user.password
    user.update(db, params.model_dump())
    return R.ok()


@router.delete('/')
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin_user)):
    user = User.get(db, user_id)
    user.delete(db)
    return R.ok()
