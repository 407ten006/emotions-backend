async def test_create_emotions__모델_테스트(async_client):
    response = await async_client.post("/api/v1/emotions/clova-test", json={"memo": "오늘 맛있는걸 먹었어"})

    assert response.status_code == 200
    assert response.json() == {}
