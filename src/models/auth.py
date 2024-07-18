from sqlmodel import Field, SQLModel


class AuthToken(SQLModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
