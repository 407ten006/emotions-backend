from sqlmodel import SQLModel


class NaverLoginData(SQLModel):
    code: str
    state: str


class AuthToken(SQLModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokenPayload(SQLModel):
    sub: str | None = None
    exp: int | None = None
