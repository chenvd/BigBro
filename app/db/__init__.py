from pathlib import Path
from sqlalchemy import create_engine, QueuePool
from sqlalchemy.orm import sessionmaker, scoped_session

from app.db.models import Base
from app.middleware.requestvars import g

db_path = Path(f'{Path(__file__).cwd()}/config')
if not db_path.exists():
    db_path.mkdir()

engine = create_engine(f'sqlite:///{db_path}/app.db',
                       pool_pre_ping=True,
                       echo=False,
                       poolclass=QueuePool,
                       pool_size=1024,
                       pool_recycle=3600,
                       pool_timeout=180,
                       max_overflow=10,
                       connect_args={"timeout": 60},
                       )

SessionFactory = sessionmaker(bind=engine, autocommit=False)


# Dependency
def get_db():
    db = SessionFactory()
    g().db = db
    try:
        yield db
    finally:
        delattr(g(), 'db')
        db.close()
