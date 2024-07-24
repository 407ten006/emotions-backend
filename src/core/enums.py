from enum import Enum


class SocialProviderEnum(Enum):
    naver = "naver"


class EmotionEnum(Enum):
    열정이 = 1  # 열정
    기쁨이 = 2  # 기쁨
    감동이 = 3  # 감동
    불안이 = 4  # 불안
    버럭이 = 5  # 버럭
    슬픔이 = 6  # 슬픔


def get_emotion_name(emotion_id: int) -> str:
    for emotion in EmotionEnum:
        if emotion.value == emotion_id:
            return emotion.name
    return None  # 해당하는 emotion_id가 없는 경우
