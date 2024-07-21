from sqlalchemy import Engine, create_engine
from sqlmodel import Session

from src.core.config import settings
from src.models import Diary, Emotion, EmotionReact, MonthlyReport, User

if settings.ENVIRONMENT == "test":
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session, engine: Engine) -> None:
    User.metadata.create_all(engine)
    Diary.metadata.create_all(engine)
    EmotionReact.metadata.create_all(engine)
    Emotion.metadata.create_all(engine)
    MonthlyReport.metadata.create_all(engine)
