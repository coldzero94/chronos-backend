# Chronos Stratege

LLM 기반 캘린더 어시스턴트

## 환경 설정

### 필수 요구사항
- Python 3.11
- Poetry
- PostgreSQL 15+
- Redis

### 개발 환경 설정

1. Python 3.11 설치 (pyenv 사용)
```bash
# pyenv로 Python 설치
pyenv install 3.11.7
pyenv local 3.11.7
```

2. Poetry 설치 및 의존성 설치
```bash
# Poetry 설치
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install
```

3. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 수정하여 필요한 환경 변수 설정
# - Database 설정
# - Google OAuth 인증 정보
# - AWS 인증 정보
# - OpenAI API 키
```

4. 개발 서버 실행
```bash
poetry shell  # 가상환경 활성화
uvicorn app.main:app --reload
```

## 프로젝트 구조
```
/app
├── api/              # API 엔드포인트
├── core/             # 핵심 설정 및 유틸리티
├── models/           # 데이터베이스 모델
├── services/         # 비즈니스 로직
└── utils/            # 유틸리티 함수
```

## API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc