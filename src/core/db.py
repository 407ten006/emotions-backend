from core.config import settings
from cruds import emotions as emotions_crud
from models import Diary, EmotionReact, MonthlyReport, User
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, select

if settings.ENVIRONMENT == "test":
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# async def init_data(session: Session) -> None:
#     if not session.exec(select(Emotion)).first():
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="열정이", description="열정이"))
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="기쁨이", description="기쁨이"))
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="감동이", description="감동이"))
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="불안이", description="불안이"))
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="버럭이", description="버럭이"))
#     await emotions_crud.create_emotion(session=session, emotion_create=EmotionCreate(name="슬픔이", description="슬픔이"))


async def init_db(session: Session, engine: Engine) -> None:
    User.metadata.create_all(engine)
    Diary.metadata.create_all(engine)
    EmotionReact.metadata.create_all(engine)
    # Emotion.metadata.create_all(engine)
    MonthlyReport.metadata.create_all(engine)

    # if settings.ENVIRONMENT in ("local", "test"):
    #     await init_data(session)
