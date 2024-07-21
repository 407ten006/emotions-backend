from datetime import datetime, timedelta

from sqlmodel import Session, select

from models.diaries import Diary, DiaryCreate


def get_today_diary(
    *, session: Session, user_id: int, search_date_yymmdd: str
) -> Diary | None:
    search_date = datetime.strptime(search_date_yymmdd, "%Y%m%d")
    statement = (
        select(Diary)
        .where(Diary.user_id == user_id)
        .where(Diary.created_datetime >= search_date)
        .where(Diary.created_datetime < search_date + timedelta(days=1))
    )
    return session.exec(statement).first()


def get_diaries_by_month(
    *, session: Session, user_id: int, search_date_yymm: str
) -> list[Diary]:
    statement = (
        select(Diary)
        .where(Diary.user_id == user_id)
        .where(Diary.created_datetime == search_date_yymm)
    )
    return session.exec(statement).all()


def create_diary(*, session: Session, diary_in: DiaryCreate) -> Diary:
    diary = Diary.from_orm(diary_in)

    session.add(diary)
    session.commit()
    session.refresh(diary)
    return diary


def update_main_emotion(*, session: Session, diary: Diary, emotion_id: int) -> Diary:
    diary.chosen_emotion_id = emotion_id

    session.add(diary)
    session.commit()
    session.refresh(diary)

    return diary


def get_diary_by_id(*, session: Session, diary_id: int) -> Diary | None:
    return session.get(Diary, diary_id)
