from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel


def custom_encoder(obj):
    if isinstance(obj, SQLModel):
        return obj.model_dump()
    return obj


def create_response(
    success: bool, message: str, data: dict | list | None = None, status_code: int = 200
):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {"success": success, "message": message, "data": data},
            custom_encoder={SQLModel: lambda obj: obj.model_dump()},
        ),
    )
