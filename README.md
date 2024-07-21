# 감정 캘린더 (가칭)

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