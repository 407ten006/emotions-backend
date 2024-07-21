from datetime import datetime, timedelta

from sqlmodel import Session, select

from models.diaries import Diary, DiaryCreate
from models.emotion_reacts import EmotionReactCreate
from models import EmotionReact


def create_emotion_react(*,session: Session, emotion_react_in: EmotionReactCreate) -> EmotionReact:
    emotion_react = EmotionReact.from_orm(emotion_react_in)
    session.add(emotion_react)
    session.commit()
    session.refresh(emotion_react)
    return emotion_react