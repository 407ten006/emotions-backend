from models import Emotion
from models.emotions import EmotionCreate, EmotionUpdate
from sqlmodel import Session, select


# TODO: 거의 변경되지 않는 정보이므로, 내부 캐싱을 통해 불필요한 쿼리를 줄일 수 있음
async def get_emotion_by_id(*, session: Session, emotion_id: int) -> Emotion:
    return session.get(Emotion, emotion_id)


async def get_emotion_by_name(*, session: Session, name: str) -> Emotion:
    return session.exec(select(Emotion).where(Emotion.name == name)).first()


async def get_emotions(*, session: Session) -> list[Emotion]:
    return session.exec(select(Emotion)).all()


async def create_emotion(*, session: Session, emotion_create: EmotionCreate) -> Emotion:
    emotion = Emotion.from_orm(emotion_create)

    session.add(emotion)
    session.commit()
    session.refresh(emotion)
    return emotion


async def update_emotion(
    *, session: Session, emotion: Emotion, emotion_update: EmotionUpdate
) -> Emotion:
    update_data = emotion_update.model_dump(exclude_unset=True)

    emotion = emotion.sqlmodel_update(update_data)
    session.add(emotion)
    session.commit()
    session.refresh(emotion)

    return emotion
