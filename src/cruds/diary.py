from sqlmodel import Session

from models import Diary


async def add_diary(session: Session, diary: Diary):
    session.add(diary)
