from sqlmodel import Field, SQLModel


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


class EmotionPublic(EmotionBase):
    id: int


class EmotionsPublic(SQLModel):
    data: list[EmotionPublic]
    count: int
