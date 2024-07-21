import json

import requests


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        complete_message = []
        parsed_data = None
        headers = {
            "X-NCP-CLOVASTUDIO-API-KEY": self._api_key,
            "X-NCP-APIGW-API-KEY": self._api_key_primary_val,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }
        flag = False
        with requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003",
            headers=headers,
            json=completion_request,
            stream=True,
        ) as r:
            for line in r.iter_lines():
                decoded_line = line.decode("utf-8")
                if line:
                    if flag:
                        data = json.loads(decoded_line[5:])
                        parsed_data = data["message"]["content"]
                        flag = False
                    if decoded_line == "event:result":
                        flag = True

            # print(complete_message)
            print(parsed_data)
            if parsed_data:
                # JSON 데이터를 파싱한 후 딕셔너리로 변환
                if isinstance(parsed_data, str):
                    parsed_data = json.loads(parsed_data)
                emotion_analysis = parsed_data.get("감정 분석", {})
                emotion_percentages = parsed_data.get("감정 퍼센트", {})
                return emotion_analysis, emotion_percentages
