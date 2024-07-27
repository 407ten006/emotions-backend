import pytest
from core.config import settings
from httpx import AsyncClient
from models import User
from models.auth import AuthToken
from models.diaries import Diary, DiaryCreate
from models.emotion_reacts import EmotionReact, EmotionReactCreate
from sqlmodel import Session

pytestmark = pytest.mark.asyncio


async def test__get_today_diary__오늘_기록이_없는_경우(
    async_client: AsyncClient, sample_user: User, login_sample_user: AuthToken
):
    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/today",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )

    response_json = response.json()
    print(response_json)
    assert response.status_code == 404


async def test__get_today_diary__오늘_기록이_있는_경우(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘의 일기",
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/today",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )
    print(response.json())


async def test_get_month_diaries_특정달의_다이어리들_조회(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘의 일기",
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
        params={"search_date_yymm": "202407"},
    )

    print("Response", response.json())


async def test_create_diary_api_다이어리_생성(
    mocker,
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    # mocker.patch(
    #     "core.clova_model_api.CompletionExecutor.execute",
    #     return_value={
    #         "emotions": {
    #             "기쁨이": "놀이공원에서 친구들과 즐거운 시간을 보내서 정말 좋았겠다! 놀이기구를 타면서 신나게 웃고, 따뜻한 햇살도 느낄 수 있었다니, 정말 행복한 하루였을 것 같아. 물론 우산을 잃어버린 건 속상하지만, 그래도 친구들과 함께한 추억이 있으니까 괜찮아!",
    #             "슬픔이": "좋아하는 우산을 잃어버려서 정말 속상했겠다. 물건을 잃어버리는 건 언제나 슬픈 일이니까. 그래도 친구들과 함께한 좋은 추억이 있어서 조금이나마 위로가 될 수 있을 거야.",
    #             "버럭이": "우산을 잃어버리다니! 너무 화가 나겠다. 놀이공원에서 즐거운 시간을 보낸 것도 중요하지만, 물건을 잃어버리는 건 정말 짜증나는 일이지. 그래도 친구들과 함께한 추억을 생각하면서 마음을 가라앉혀 봐.",
    #         },
    #         "percentage": {"기쁨이": 75, "슬픔이": 20, "버럭이": 5},
    #     },
    # )

    user_input = "오늘은 정말 특별한 날이었다. 오랜만에 친구들과 함께 놀이공원에 갔다. 놀이기구를 타면서 모두가 신나게 웃었고, 햇살도 따뜻하게 우리를 감싸주었다. 그런데 집으로 돌아오는 길에 우산을 잃어버린 것을 알았다. 그래도 친구들과의 추억 덕분에 하루가 행복하게 마무리되었다. !"

    response = await async_client.post(
        f"{settings.API_V1_STR}/diaries/",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
        json={"content": user_input},
    )

    print(response.json())



async def test_create_diary_api_다이어리_생성_다중_테스트(
    mocker,
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    # mocker.patch(
    #     "core.clova_model_api.CompletionExecutor.execute",
    #     return_value={
    #         "emotions": {
    #             "기쁨이": "놀이공원에서 친구들과 즐거운 시간을 보내서 정말 좋았겠다! 놀이기구를 타면서 신나게 웃고, 따뜻한 햇살도 느낄 수 있었다니, 정말 행복한 하루였을 것 같아. 물론 우산을 잃어버린 건 속상하지만, 그래도 친구들과 함께한 추억이 있으니까 괜찮아!",
    #             "슬픔이": "좋아하는 우산을 잃어버려서 정말 속상했겠다. 물건을 잃어버리는 건 언제나 슬픈 일이니까. 그래도 친구들과 함께한 좋은 추억이 있어서 조금이나마 위로가 될 수 있을 거야.",
    #             "버럭이": "우산을 잃어버리다니! 너무 화가 나겠다. 놀이공원에서 즐거운 시간을 보낸 것도 중요하지만, 물건을 잃어버리는 건 정말 짜증나는 일이지. 그래도 친구들과 함께한 추억을 생각하면서 마음을 가라앉혀 봐.",
    #         },
    #         "percentage": {"기쁨이": 75, "슬픔이": 20, "버럭이": 5},
    #     },
    # )

    user_input_array = [
        # "오늘은 정말 특별한 날이었다. 오랜만에 친구들과 함께 놀이공원에 갔다. 놀이기구를 타면서 모두가 신나게 웃었고, 햇살도 따뜻하게 우리를 감싸주었다. 그런데 집으로 돌아오는 길에 우산을 잃어버린 것을 알았다. 그래도 친구들과의 추억 덕분에 하루가 행복하게 마무리되었다. !",
        "오늘은 아주 특별한 날이었다. 오랜만에 친구들과 함께 모여 도심 속 작은 카페에서 이야기를 나눴다. 바쁜 일상 속에서 이렇게 여유로운 시간을 가지니 마음이 한결 가벼워졌다. 특히, 카페의 따뜻한 커피와 맛있는 디저트가 우리의 대화를 더욱 풍성하게 해주었다. 친구들과의 웃음 소리에 시간 가는 줄도 몰랐다. 집으로 돌아오는 길에 노을이 지는 하늘을 보며 오늘 하루가 참 행복했다고 느꼈다.",
        "오늘은 가족들과 함께 산책을 다녀왔다. 가까운 공원으로 나가니, 여름이 성큼 다가온 느낌이었다. 공원에는 다양한 꽃들이 만개해 있었고, 향긋한 꽃내음이 코끝을 간지럽혔다. 우리는 벤치에 앉아 시원한 바람을 맞으며 서로의 이야기를 나눴다. 평소에 못했던 이야기들을 나누며 더욱 가까워진 기분이었다. 집으로 돌아오는 길에는 아이스크림을 사서 먹었는데, 여름의 시작을 느끼기에 충분했다.",
        "오늘은 회사에서 중요한 발표가 있는 날이었다. 아침부터 긴장이 많이 됐지만, 동료들의 격려 덕분에 무사히 발표를 마칠 수 있었다. 준비한 내용이 잘 전달되었는지 반응이 좋아서 뿌듯했다. 발표가 끝난 후, 팀원들과 함께 점심을 먹으며 서로를 격려했다. 긴장된 하루였지만, 많은 것을 배우고 성장할 수 있는 기회였다. 집에 돌아와서 오늘 하루를 돌아보니, 앞으로도 최선을 다해야겠다는 다짐이 생겼다.",
        "오늘은 비가 내리는 날이었다. 창밖을 보며 차분하게 책을 읽는 시간을 가졌다. 평소 바쁘게 지내느라 미뤄둔 책을 드디어 끝낼 수 있었다. 비 소리를 들으며 조용히 책에 몰입하는 시간이 정말 힐링이 되었다. 점심에는 집에서 간단히 파스타를 만들어 먹었는데, 생각보다 맛있게 잘 되어서 기분이 좋았다. 비 오는 날의 여유로운 하루를 보내며 마음이 한결 평온해졌다.",
        "오늘은 운동을 하기로 한 날이었다. 아침 일찍 일어나서 근처 헬스장에 갔다. 처음에는 조금 힘들었지만, 점점 몸이 적응하면서 운동이 즐거워졌다. 트레이너의 도움을 받아 새로운 운동법도 배웠다. 운동을 마치고 나니 땀으로 젖은 몸이 상쾌했다. 집에 돌아와 샤워를 하고 나니 하루가 활기차게 시작되는 느낌이었다. 앞으로도 꾸준히 운동을 해야겠다고 다짐했다.",
        "오늘은 회사에서 새로운 프로젝트를 시작하는 날이었다. 팀원들과 함께 회의를 하며 계획을 세우고 역할을 분담했다. 처음에는 막막했지만, 모두가 협력하여 하나씩 문제를 해결해 나가는 과정이 흥미로웠다. 점심시간에는 팀원들과 함께 맛있는 점심을 먹으며 친목을 다졌다. 하루가 끝나고 나니 피곤했지만, 뭔가 큰 일을 해냈다는 뿌듯함이 느껴졌다. 앞으로 이 프로젝트가 잘 진행되기를 기대해본다.",
        "오늘은 오랜만에 집에서 요리를 했다. 인터넷에서 찾은 새로운 레시피를 따라 해본 결과, 생각보다 훌륭한 요리가 완성되었다. 가족들도 맛있게 먹어줘서 기분이 좋았다. 요리를 하면서 느낀 건, 손으로 무언가를 만드는 것이 참 즐겁다는 것이다. 저녁 식사를 마치고 가족들과 함께 영화를 보며 하루를 마무리했다. 따뜻한 집에서 보내는 시간이 참 소중하게 느껴진 하루였다.",
        "오늘은 동네 도서관에 다녀왔다. 조용한 도서관에서 책을 읽는 시간이 참 좋았다. 평소에 관심 있었던 주제의 책을 빌려와서 하루 종일 읽었다. 책을 통해 새로운 지식과 아이디어를 얻을 수 있어서 매우 유익한 시간이었다. 도서관에서의 평온한 분위기가 마음을 차분하게 해주었다. 집으로 돌아와서도 책 속의 이야기들을 곱씹으며 하루를 보냈다. 앞으로도 자주 도서관에 가야겠다.",
        "오늘은 새로운 취미로 시작한 그림 그리기를 했다. 캔버스 앞에 앉아 마음 가는 대로 색을 칠하는 시간이 참 즐거웠다. 처음에는 서툴렀지만, 점점 손에 익으면서 나만의 그림이 완성되어 갔다. 그림을 그리면서 하루 동안의 스트레스가 모두 해소되는 느낌이었다. 완성된 작품을 보니 뿌듯했다. 앞으로도 꾸준히 그림을 그리며 나만의 작품을 더 많이 만들어 보고 싶다.",
        "오늘은 친구와 함께 자전거를 타고 근교로 나들이를 다녀왔다. 맑은 날씨에 자전거를 타니 상쾌한 바람이 기분 좋았다. 길가에 피어있는 꽃들을 구경하며 여유롭게 자전거를 타다가, 한적한 공원에서 잠시 쉬었다. 공원에서 먹는 간식은 평소보다 더 맛있게 느껴졌다. 돌아오는 길에는 일몰을 보며 아름다운 풍경에 감탄했다. 오랜만에 자연 속에서 보내는 시간이 힐링이 되었다.",
        "오늘은 회사에서 팀 빌딩 행사가 있었다. 모두가 한 자리에 모여 다양한 게임을 즐기며 서로를 더 잘 알게 되는 시간이 되었다. 특히, 보물찾기 게임에서 내가 속한 팀이 우승을 해서 기분이 좋았다. 평소 업무로 인해 느꼈던 스트레스도 잠시 잊고, 동료들과 웃고 떠들며 즐거운 시간을 보냈다. 이런 시간이 종종 필요하다는 것을 새삼 느꼈다. 집에 돌아와서도 행사의 여운이 남아 하루 종일 기분이 좋았다.",
        "오늘은 집에서 쉬면서 책을 읽었다. 오랜만에 손에 잡은 소설이었는데, 이야기가 너무 흥미로워서 시간 가는 줄 몰랐다. 중간중간 차를 마시며 여유롭게 독서하는 시간이 정말 힐링이 되었다. 책 속의 주인공과 함께 모험을 떠나는 기분이 들었다. 오후에는 간단히 산책을 다녀오며 머리를 식히기도 했다. 집으로 돌아와서는 저녁을 준비하며 하루를 마무리했다. 이렇게 여유로운 하루가 가끔은 필요하다.",
        "오늘은 아침 일찍 일어나서 요가를 했다. 평소에 운동을 자주 하지 못했는데, 몸을 움직이니 기분이 상쾌해졌다. 요가를 통해 몸과 마음이 모두 정화되는 느낌이었다. 이후에는 건강한 아침 식사를 준비해서 먹었다. 신선한 과일과 요거트를 곁들인 식사 덕분에 에너지가 넘쳤다. 하루 종일 기분 좋게 일을 할 수 있었고, 효율도 높아졌다. 앞으로는 아침 요가를 꾸준히 해봐야겠다고 다짐했다.",
        "오늘은 친구들과 함께 영화관에 다녀왔다. 오랜만에 보는 영화라 기대가 컸다. 영화는 기대 이상으로 재미있었고, 친구들과 함께여서 더욱 즐거웠다. 팝콘과 음료를 나눠 먹으며 웃고 떠드는 시간이 정말 소중하게 느껴졌다. 영화가 끝난 후에는 근처 카페에 가서 디저트를 먹으며 영화에 대한 이야기를 나눴다. 친구들과 함께하는 시간이 이렇게 소중한 줄 다시 한번 깨달았다. 오늘 하루도 행복하게 마무리할 수 있었다.",
        "오늘은 날씨가 좋아서 자전거를 타고 공원에 다녀왔다. 맑은 하늘 아래서 자전거를 타니 상쾌한 기분이 들었다. 공원에 도착해서는 벤치에 앉아 책을 읽기도 하고, 주변을 산책하기도 했다. 나무와 꽃들이 만개해 있어서 눈이 즐거웠다. 자전거를 타고 돌아오는 길에는 시원한 바람이 기분 좋게 불어왔다. 집에 도착해서는 가벼운 스트레칭을 하며 몸을 풀었다. 오늘 하루는 자연 속에서의 힐링 타임이었다."
    ]
    # user_input_array = [
    #     "오늘은 친구와 함께 자전거를 타고 근교로 나들이를 다녀왔다. 맑은 날씨에 자전거를 타니 상쾌한 바람이 기분 좋았다. 길가에 피어있는 꽃들을 구경하며 여유롭게 자전거를 타다가, 한적한 공원에서 잠시 쉬었다. 공원에서 먹는 간식은 평소보다 더 맛있게 느껴졌다. 돌아오는 길에는 일몰을 보며 아름다운 풍경에 감탄했다. 오랜만에 자연 속에서 보내는 시간이 힐링이 되었다."
    # ]

    for i in range(len(user_input_array)):
        print(user_input_array[i])
        response = await async_client.post(
            f"{settings.API_V1_STR}/diaries/",
            headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
            json={"content": user_input_array[i]},
        )

        print(response)
async def test_get_diary_특정_다이어리_조회(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):

    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘의 일기",
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    emotion_react_create = EmotionReactCreate(
        diary_id=diary.id, emotion_id=1, content="정말 기뻐요!", percent=80
    )

    emotion_react = EmotionReact.from_orm(emotion_react_create)
    db_session.add(emotion_react)
    db_session.commit()
    db_session.refresh(emotion_react)

    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/{diary.id}",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )
    print(response.json())


async def test_update_main_emotion_메인감정_업데이트(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘의 일기",
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    response = await async_client.patch(
        f"{settings.API_V1_STR}/diaries/{diary.id}",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
        json={"main_emotion_id": 1},
    )

    print(response.json())
