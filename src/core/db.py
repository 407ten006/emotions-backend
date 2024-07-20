from sqlmodel import Session, create_engine

from src.core.config import settings
from src.models.emotions import Emotion
from src.models.users import User, Diary

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    User.metadata.create_all(engine)
    Diary.metadata.create_all(engine)
    Emotion.metadata.create_all(engine)
