import json

import requests


class BadExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, user_input) -> bool | None:

        # before execute
        if user_input == "exit":
            return

        preset_text = [
            {
                "role": "system",
                "content": "- 당신은 닉네임에 비속어 혹은 욕설이 포함되어있는지 판별하는 시스템입니다. \n- 응답은 항상 JSON 형태로 반환해주세요.\n- 주어진 사용자의 닉네임에 "
                '비속어 혹은 욕설이 포함되어 있는지 여부에 따라 아래와 같이 응답해주세요. \n\n## 비속어가 포함된 경우\n{"clean":false}\n\n\n## 비속어가 '
                '포함되지 않은 경우\n{"clean":true}',
            },
            {"role": "user", "content": user_input},
        ]

        headers = {
            "X-NCP-CLOVASTUDIO-API-KEY": self._api_key,
            "X-NCP-APIGW-API-KEY": self._api_key_primary_val,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }

        request_data = {
            "messages": preset_text,
            "topP": 0.8,
            "topK": 0,
            "maxTokens": 256,
            "temperature": 0.7,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": True,
            "seed": 0,
        }

        flag = False
        parsed_data = None

        with requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003",
            headers=headers,
            json=request_data,
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
        try:
            parsed_json = json.loads(parsed_data)
            return parsed_json["clean"]

        except json.JSONDecodeError:
            return None
