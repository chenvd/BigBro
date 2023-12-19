import types

import fastapi
from fastapi import FastAPI
from fastapi.responses import Response
from app.api import api_router
from app.db.init import init_db
from app.exception import AuthorizationException, AccessDeniedException, BizException
from app.middleware import requestvars
from app.scheduler import Scheduler, scheduler

app = FastAPI()


@app.on_event("startup")
def on_startup():
    app.include_router(api_router)
    init_db()
    scheduler.init()


@app.middleware('http')
async def init_request_vars(request: fastapi.Request, call_next):
    initial_g = types.SimpleNamespace()
    requestvars.request_global.set(initial_g)
    response = await call_next(request)
    return response


@app.exception_handler(AuthorizationException)
def handle_authorization_exception(*_: any):
    return Response('身份验证失败', status_code=401)


@app.exception_handler(AccessDeniedException)
def handle_access_denied_exception(*_: any):
    return Response('您无权访问此操作', status_code=403)


@app.exception_handler(BizException)
def handle_biz_exception(_, exc: BizException):
    return Response(exc.detail, status_code=400)


if __name__ == '__main__':
    pass
