import json
from typing import Any

from fastapi import APIRouter, Request, HTTPException

from core.clova_model_api import CompletionExecutor

router = APIRouter()


@router.post("/clova-test")
async def clova_test(request: Request) -> Any:
    """
    클로바 테스트

    """
    # 클로바 API 분석

    try:
        body_bytes = await request.body()
        body = json.loads(body_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    user_input = body.get("content")
    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6",
        api_key_primary_val="K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q",
        request_id="b109906c-e945-4c19-9d30-8bd62bd8f0a7",
    )


    response_data = completion_executor.execute(user_input)
    if response_data == None:
        return HTTPException(status_code=404, detail="Not Found")
    else:
        return response_data
