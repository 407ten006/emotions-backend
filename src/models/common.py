from sqlmodel import SQLModel


class ResponseMessage(SQLModel):
    message: str
