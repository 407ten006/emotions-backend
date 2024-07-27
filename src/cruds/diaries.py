from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from models.diaries import Diary, DiaryCreate
from sqlmodel import Session, func, select


async def get_today_diary(
    *, session: Session, user_id: int, kst_search_date_yymmdd: str
) -> Diary | None:
    search_date = datetime.strptime(kst_search_date_yymmdd, "%Y%m%d")

    # UTC 기준으로 검색 범위 설정
    utc_start = search_date.astimezone(ZoneInfo("UTC"))
    utc_end = (search_date + timedelta(days=1)).astimezone(ZoneInfo("UTC"))

    statement = (
        select(Diary)
        .where(Diary.user_id == user_id)
        .where(Diary.created_datetime >= utc_start)
        .where(Diary.created_datetime < utc_end)
    )
    return session.exec(statement).first()


async def get_diaries_by_month(
    *, session: Session, user_id: int, search_date_yymm: str
) -> list[Diary]:
    year = int(search_date_yymm[:4])
    month = int(search_date_yymm[4:6])
    statement = select(Diary).where(
        (Diary.created_datetime >= datetime(year, month, 1))
        & (Diary.created_datetime < datetime(year, month + 1, 1))
        & (Diary.user_id == user_id)
    )
    return session.exec(statement).all()


async def create_diary(*, session: Session, diary_create: DiaryCreate) -> Diary:
    diary = Diary.from_orm(diary_create)

    session.add(diary)
    session.commit()
    session.refresh(diary)
    return diary


async def update_main_emotion(
    *, session: Session, diary: Diary, emotion_id: int
) -> Diary:
    diary.chosen_emotion_id = emotion_id

    session.add(diary)
    session.commit()
    session.refresh(diary)

    return diary


async def get_diary_by_id(*, session: Session, diary_id: int) -> Diary | None:
    statement = select(Diary).where(Diary.id == diary_id)
    return session.exec(statement).first()


async def get_most_common_emotion_for_month(
    *, session: Session, user_id: int, search_date_yymm: str
) -> int | None:
    year = int(search_date_yymm[:4])
    month = int(search_date_yymm[4:6])
    start_date = datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)

    statement = (
        select(
            Diary.chosen_emotion_id, func.count(Diary.chosen_emotion_id).label("count")
        )
        .where(
            Diary.user_id == user_id,
            Diary.created_datetime >= start_date,
            Diary.created_datetime < end_date,
        )
        .group_by(Diary.chosen_emotion_id)
        .order_by(func.count(Diary.chosen_emotion_id).desc())
    )

    result = session.exec(statement).first()
    if result:
        return result.chosen_emotion_id
    return None
