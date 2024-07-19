from sqlmodel import Session, select

from src.models.users import User, UserCreate, UserUpdateMe


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User(**user_create.dict())
    print(db_obj)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def update_user(*, session: Session, user: User, user_update: UserUpdateMe) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    user.sqlmodel_update(update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def is_already_exist_nickname(*, session: Session, nickname: str) -> bool:
    statement = select(User).where(User.nickname == nickname)
    return session.exec(statement).first() is not None
