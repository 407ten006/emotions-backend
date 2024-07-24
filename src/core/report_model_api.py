import json

import requests


class ReportExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, user_input) -> dict | None:

        # before execute
        preset_text = [
            {
                "role": "system",
                "content": "- 입력된 감정을 기반으로 사용자에게 할 수 있는 조언들을 해줍니다\n- 입력된 감정은 유저가 한달전체에서 느낀 감정 중 가장 많은 부분은 차지한 감정이 "
                "입력됩니다. \n- 입력되는 감정들은 기쁨, 슬픔, 열정, 불안, 버럭,  감동 총 6가지 입니다\n- 입력된 감정들에 대한 조언을 하되, 여러 감정들과 조화를 "
                "이루는 방법에 대해서 설명하면 더 좋습니다. \n\n\n\n\n입력: 기쁨\n출력 : 이번 달에는 기쁨이가 가장 많았네요!\n사용자님의 한 달이 기쁨으로 가득 "
                "채워진 것 같아 보기 좋아요.\n그러나, 혹시 사용자님이 슬픈 감정을 억누르고 있지는 않았는지 다시 한 번 생각해보세요. 문제가 생겼을때, "
                "가끔은 기쁨으로 이겨내기보다는 슬픔을 자연스럽게 표현하는 것이 더 좋은 해결책이 될 수 있어요.\n\n\n입력: 열정\n출력 : 모든 일에 열정 넘치는 모습, "
                "훌륭해요!! 좋아하는 일에 열정적으로 임하는 것은 무엇보다 중요하죠. 하지만 너무 열정이 넘쳐, 자신을 위한 시간이 부족하지는 않았는지 한번 더 "
                "확인해보세요!\n\n\n입력:슬픔\n출력: 슬픔이가 많은 달이었네요!\n 슬픔은 삶의 의미와 가치를 깨닫게 해주는 중요한 감정입니다. 슬픔을 통해 우리는 소중한 "
                "것들을 인식하고 성장할 수 있어요.\n 하지만 슬픔만 지속되면 우울감과 무기력감으로 이어질 수 있어, 다양한 감정들이 조화롭게 공존하는 것이 중요합니다. \n "
                "기쁨, 분노, 공포 등 다른 기본 감정들도 우리의 삶에 중요한 역할을 합니다. 이러한 감정들을 갖기 위해, 우선 하루에 하나씩 사소한 일이라도 나의 하루를 "
                "기쁘게 한 일을 기록해보는 건 어떨까요?\n 하루에 하나의 행복한 일이 쌓이고 쌓이면, 어느덧 큰 행복으로 다가올 거에요! 사용자님의 8월도 응원할게요 :)",
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
            "temperature": 0.5,
            "repeatPenalty": 5.0,
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

        return parsed_data
