from typing import Union

from fastapi.responses import JSONResponse

def create_response(success: bool, message: str, data: Union[dict, list, None] = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "message": message,
            "data": data
        }
    )
