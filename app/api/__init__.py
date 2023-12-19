from fastapi import APIRouter, Depends

from app.api import auth, user, rule, notify, home, setting
from app.dependencies.security import verify_token

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(user.router, prefix='/user', dependencies=[Depends(verify_token)])
api_router.include_router(rule.router, prefix='/rule', dependencies=[Depends(verify_token)])
api_router.include_router(notify.router, prefix='/notify', dependencies=[Depends(verify_token)])
api_router.include_router(home.router, prefix='/home', dependencies=[Depends(verify_token)])
api_router.include_router(setting.router, prefix='/setting', dependencies=[Depends(verify_token)])
