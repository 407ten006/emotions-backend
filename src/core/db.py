from core.config import settings
from models import Diary, EmotionReact, MonthlyReport, User
from sqlalchemy import Engine, QueuePool, create_engine
from sqlmodel import Session

if settings.ENVIRONMENT == "test":
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}
    )
else:
    dbschema = "db,public"

    engine = create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        poolclass=QueuePool,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        connect_args={"options": f"-c search_path={dbschema}"},
    )


async def init_db(session: Session, engine: Engine) -> None:
    User.metadata.create_all(engine)
    Diary.metadata.create_all(engine)
    EmotionReact.metadata.create_all(engine)
    MonthlyReport.metadata.create_all(engine)
