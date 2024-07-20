import pytest
import requests
import json
import time

from api.clova_model_api import CompletionExecutor

@pytest.mark.asyncio
async def test_create_emotions__모델_테스트(async_client):
    print("start")
    response = await async_client.post("/api/v1/emotions/clova-test", json={"content": "오늘 맛있는걸 먹었어"})
    print("response", response)
    # assert response.status_code == 200
    # assert response.json() == {}

def 단순_모델_테스트(user_input):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6',
        api_key_primary_val='K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q',
        request_id='b109906c-e945-4c19-9d30-8bd62bd8f0a7'
    )

    if user_input == "exit":
        return
    preset_text = [{"role": "system",
                    "content": "- 주어진 글을 보고 기쁨, 슬픔, 버럭이, 열정이, 감동이, 불안이의 관점에서 말할 내용을 작성해주세요.\n- 각 감정들은 개별적이며, 해당 감정들의 감정만 묘사를 해야 합니다.\n- 해당 감정에만 충실하세요.\n- 글의 내용에만 충실해야 합니다. 새로운 가정을 들어서 판단을 하면 안됩니다. \n- 기록에 해당 감정이 없다면 그 감정은 표현할 필요 없습니다. \n- 억지로 감정을 만들어내서 표현할 필요는 없습니다. 이건 매우 중요합니다. \n-  최소 1개 이상의 감정은 나타나야 합니다. \n- 주어진 글에 대한 감정의 퍼센트를 나타내는 요약이 담겨있어야 합니다.\n-  감정퍼센트의 전체합은 100 %가 되어야 합니다. \n- 감정을 좀 더 풍부하게 표현해줘. 이모티콘도 써도 상관없어\n- 너무 딱딱하게 말하지 않았으면 좋겠어\n- JSON 으로 결과를 보여줘\n\n###\n기록: 오늘은 정말 특별한 날이었다. 오랜만에 친구들과 함께 놀이공원에 갔다. 놀이기구를 타면서 모두가 신나게 웃었고, 햇살도 따뜻하게 우리를 감싸주었다. 그런데 집으로 돌아오는 길에 우산을 잃어버린 것을 알았다. 그래도 친구들과의 추억 덕분에 하루가 행복하게 마무리되었다. \n\n\n{\n  \"감정 분석\": {\n    \"버럭이\": \"뭐야! 우산을 잃어버리다니! 그게 얼마나 중요한 건데! 놀이공원에서 아무리 재미있었다고 해도, 이렇게 중요한 걸 잃어버리면 어떡해!\",\n    \"기쁨이\": \"재밌었겠다! 우산 그거, 또 사면 되지! 친구들이랑 같이 놀이공원이라니, 생각만 해도 두근거리는데 ><\",\n    \"슬픔이\": \"분명 좋아하던 우산이었을텐데..! 나같으면 펑펑 울었어ㅠㅠㅠㅠㅠㅠㅠ. 중요한 걸 잃어버리는 건 슬픈 일이잖아.\",\n    \"불안이\": \"우산을 잃어버렸다니, 이제 비가 오면 어떻게 하지? 다음에 또 놀이공원에 갈 때도 뭔가 잃어버리면 어쩌지? 중요한 걸 잃어버리면 항상 마음이 불안해.\",\n    \"열정이\": \"놀이공원! 친구들과 함께 놀이기구를 타고 신나게 웃었구나! 그런 순간들은 정말 에너지 넘치고 즐거운 경험이지. 앞으로도 이런 날들이 많이 있었으면 좋겠어!\",\n    \"감동이\": \"친구들과의 소중한 추억이라니, 정말 아름다운 시간이었겠구나. 햇살이 따뜻하게 감싸주는 그 순간들, 그리고 웃음소리들, 그런 소중한 기억이 마음 깊이 남을 거야. 우산을 잃어버린 건 아쉽지만, 그만큼 소중한 하루를 보냈다는 게 더 큰 감동이야.\"\n  },\n  \"감정 퍼센트\": {\n    \"기쁨이\": 70,\n    \"슬픔이\": 20,\n    \"버럭이\": 5,\n    \"불안이\": 3,\n    \"열정이\": 1,\n    \"감동이\": 1\n  }\n}\n\n\n"}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 558,
        'temperature': 0.91,
        'repeatPenalty': 2.93,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    emotions_analysis, emotions_percentage = completion_executor.execute(request_data)

    return emotions_analysis,emotions_percentage


user_input = "오늘은 가족들과 함께 공원에 갔다. 날씨가 너무 좋아서 피크닉을 하기로 했다. 엄마가 준비해주신 샌드위치와 과일을 먹으면서 가족들과 웃고 떠들었다. 동생과 함께 연을 날렸는데, 바람이 좋아서 높이 날아올랐다. 공원에서의 시간을 보내고 집으로 돌아오는 길에 아이스크림 가게에 들러서 디저트를 먹었다. 행복한 하루였다."

# emotions_analysis, emotions_percentage = 단순_모델_테스트(user_input)
# print(emotions_analysis,emotions_percentage)

