from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from models import EmotionReact

class EmotionBase(SQLModel):
    name: str = Field(..., max_length=20)
    description: str = Field(..., max_length=300)


class EmotionCreate(SQLModel):
    name: str = Field(..., max_length=20)
    description: str = Field(..., max_length=300)


class EmotionUpdate(SQLModel):
    name: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=300)


class Emotion(EmotionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=20)
    description: str = Field(..., max_length=300)

    emotion_reacts: list["EmotionReact"] = Relationship(back_populates="emotion")


class EmotionPublic(EmotionBase):
    id: int


class EmotionsPublic(SQLModel):
    data: list[EmotionPublic]
    count: int
