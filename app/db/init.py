from app.db import engine, SessionFactory
from app.db.models import *
from app.utils.security import get_password_hash


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionFactory() as db:
        user = db.query(User).filter_by(username='admin').one_or_none()
        if not user:
            user = User()
            user.username = 'admin'
            user.password = get_password_hash("password")
            user.name = "管理员"
            user.is_admin = True
            db.add(user)
            db.commit()
