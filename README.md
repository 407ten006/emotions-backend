# 마이모지(My Moji)

## 목적
마이모지는 감정이들을 통한 일상 기록 및 감정 분석 서비스입니다

## 목표
- Naver Clova Studio의 챗봇 AI를 커스터마이징 하여 사용자가 작성한 글에 맞는 감정들의 반응들을 보여준다
- "이달의 감정 리포트" 을 통해서 해당 달에 사용자가 어떤 감정을 가졌는지 해당 감정을 잘 활용하기 위해서는 어떻게 해야하는지에 대한 지침을 제공한다

## 팀원(Back-end)
- 현진우, 장준형

## 기술스택
- FastAPI
- postgresql
- Naver Cloud
- Naver Clova Studio

## 서비스 소개
<img width="1920" alt="1" src="https://github.com/user-attachments/assets/188b5c17-ee45-403a-9e57-1421372ce182">
<img width="1920" alt="2" src="https://github.com/user-attachments/assets/40c04f5b-7aad-4615-a55c-4724e5278366">

## 서비스 기능
<img width="1920" alt="Slide 16_9 - 6" src="https://github.com/user-attachments/assets/281bd6b4-c08e-493f-9a38-55e6dd8b90ad">

## DB 스키마
![image](https://github.com/user-attachments/assets/3b93a0ef-5fb4-43f0-9575-ae7f19554ef2)

## API Docs
[API docs](https://bumpy-bunny-koreaboardgamearena-36c727ad.koyeb.app/docs#/)

## 준비 사항

- python = "^3.10"
- poetry = "^1.8.2"

## 실행 방법

```
$ git clone <git-repository>
$ cd <git-repository>
```

### 의존성 설치

```
$ pip install poetry
$ poetry install
```

### Source Root 추가

```
# src 디렉토리를 python path에 추가
$ export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

### Local Postgres Docker 실행

```
$ docker run -d \
--name postgres-container \
--restart always \
-v app-db-data:/var/lib/postgresql/data/pgdata \
-p 5432:5432 \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-e POSTGRES_DB=app \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=4ten006! \
postgres:12
```

### 마이그레이션

```
$ alembic revision --autogenerate -m "commit message"
$ alembic upgrade head
```

```
# 임시로 core/db.py 에 추가된 모델을 등록해야합니다.

def init_db(session: Session) -> None:
    User.metadata.create_all(engine)
    Test.metadata.create_all(engine)
```

### 테스트 실행

- 환경변수 `ENVIORNMENT=test` 로 설정 후 실행해야 테스트 데이터베이스를 사용합니다. (sqlite)

## 프로젝트 구조

```

.
├── LICENSE
├── READEME.md
├── alembic.ini
├── poetry.lock
├── pyproject.toml
├── scripts
│ ├── format.sh
│ └── lint.sh
└── src
├── __init__.py
├── main.py # FastAPI app
├── alembic # 데이터베이스 마이그레이션
├── api # API 라우터
│ ├── __init__.py
│ └── v1
│ ├── __init__.py
│ ├── deps.py
│ ├── endpoints
│ │ ├── __init__.py
│ │ ├── auth.py
│ │ └── users.py
│ └── router.py
├── core # 핵심 로직
│ ├── __init__.py
│ ├── config.py
│ ├── db.py
│ ├── exceptions.py
│ ├── oauth_client.py
│ └── security.py
├── cruds # 데이터베이스 CRUD
│ ├── __init__.py
│ └── users.py
├── models # 데이터베이스 모델
│ ├── __init__.py
│ ├── auth.py
│ ├── common.py
│ └── users.py
└── utils # 유틸리티 함수
└── utils.py

```
