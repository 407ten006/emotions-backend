from sqlmodel import Session

from models import EmotionReact
from models.emotion_reacts import EmotionReactCreate


async def create_emotion_react(*,session: Session, emotion_react_in: EmotionReactCreate) -> EmotionReact:
    emotion_react = EmotionReact.from_orm(emotion_react_in)
    session.add(emotion_react)
    session.commit()
    session.refresh(emotion_react)
    return emotion_react