from sqlmodel import Session, select

from models import Diary


def add_diary(session: Session, diary: Diary):
    session.add(diary);
