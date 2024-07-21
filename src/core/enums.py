from enum import Enum


class SocialProviderEnum(Enum):
    naver = "naver"


class EmotionEnum(Enum):
    passion = "passion"  # 열정
    joy = "joy"  # 기쁨
    touched = "touched"  # 감동
    anxiety = "anxiety"  # 불안
    anger = "anger"  # 버럭
    sadness = "sadness"  # 슬픔
