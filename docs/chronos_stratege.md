# LLM 기반 캘린더 어시스턴트 기술 명세서 V2

## 1. 시스템 개요

### 1.1 프로젝트 목적
- 자연어 기반 일정 생성 및 관리
- 이미지 인식을 통한 일정 자동 생성
- 구글 계정 기반의 심플한 사용자 경험
- 구글 캘린더와의 완벽한 동기화

### 1.2 핵심 기능
- 구글 계정 기반 간편 로그인
- 자연어 처리를 통한 일정 생성
- 이미지/스크린샷 기반 일정 생성
- 실시간 대화형 일정 관리
- 구글 캘린더 자동 동기화

## 2. 기술 스택

### 2.1 백엔드
- Framework: FastAPI
- Language: Python 3.11+
- Database: PostgreSQL 15+
- ORM: SQLAlchemy 2.0
- Task Queue: Celery with Redis
- API Documentation: OpenAPI (Swagger)

### 2.2 외부 서비스 및 API
- Authentication: Google OAuth2.0
- LLM: OpenAI GPT-4
- OCR: Google Cloud Vision API
- Calendar: Google Calendar API
- Storage: AWS S3 (이미지 저장용)

## 3. 시스템 아키텍처

### 3.1 디렉토리 구조
```
/app
├── api/
│   ├── v1/
│   │   ├── auth/          # 구글 인증 관련
│   │   ├── calendar/      # 일정 관리
│   │   ├── chat/          # 대화형 인터페이스
│   │   └── image/         # 이미지 처리
├── core/
│   ├── config.py
│   ├── google_auth.py     # 구글 인증 핵심 로직
│   └── dependencies.py
├── models/
│   ├── user.py
│   ├── event.py
│   └── chat.py
├── services/
│   ├── llm_service.py
│   ├── ocr_service.py
│   ├── calendar_service.py
│   └── chat_service.py
└── utils/
    ├── image_processor.py
    └── date_parser.py
```

## 4. API 엔드포인트 명세

### 4.1 인증 API
```
POST /api/v1/auth/google/login
POST /api/v1/auth/google/refresh
POST /api/v1/auth/logout
GET /api/v1/auth/user/me
```

### 4.2 일정 관리 API
```
POST /api/v1/calendar/events
GET /api/v1/calendar/events
PUT /api/v1/calendar/events/{event_id}
DELETE /api/v1/calendar/events/{event_id}
GET /api/v1/calendar/sync           # 구글 캘린더 동기화
```

### 4.3 채팅 API
```
POST /api/v1/chat/message
GET /api/v1/chat/history
POST /api/v1/chat/process-intent
```

### 4.4 이미지 처리 API
```
POST /api/v1/image/process
POST /api/v1/image/extract-event
GET /api/v1/image/processing-status/{job_id}
```

## 5. 데이터베이스 스키마

### 5.1 Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    google_calendar_token TEXT,
    profile_image_url TEXT,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.2 Events Table
```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    location VARCHAR(255),
    attendees JSONB,
    google_event_id VARCHAR(255),
    last_synced_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.3 Chat History Table
```sql
CREATE TABLE chat_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    message TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    intent JSONB,    # 파악된 의도 저장
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 6. 핵심 기능 구현 명세

### 6.1 Google OAuth 인증 프로세스
1. 프론트엔드에서 Google OAuth 로그인 시작
2. Google OAuth 콜백으로 인증 코드 수신
3. 백엔드에서 Google OAuth 토큰 교환
4. 사용자 정보 조회 및 DB 저장/업데이트
5. JWT 액세스 토큰 발급
6. Google Calendar scope 권한 확인 및 요청

### 6.2 자연어 처리 파이프라인
1. 사용자 메시지 수신
2. LLM을 통한 의도 파악
3. 날짜/시간/장소 정보 추출
4. 필요한 추가 정보 요청
5. 일정 데이터 구조화
6. Google 캘린더 동기화

### 6.3 이미지 처리 파이프라인
1. 이미지 S3 업로드
2. OCR 비동기 처리
3. 텍스트 추출 및 정규화
4. LLM 일정 정보 추출
5. 사용자 확인 요청
6. 일정 생성 및 동기화

## 7. 보안 설정

### 7.1 인증 및 권한
- Google OAuth2.0 인증
- JWT 기반 세션 관리
- Rate Limiting 적용

### 7.2 데이터 보안
- HTTPS 통신
- Google OAuth 토큰 암호화 저장
- 개인정보 처리 로깅

## 8. 성능 요구사항

### 8.1 응답 시간
- API 응답: 300ms 이내
- 이미지 처리: 5초 이내
- 채팅 응답: 2초 이내

### 8.2 동시성 처리
- 100+ 동시 사용자 지원
- 이미지 처리 작업 큐잉
- DB 커넥션 풀링

## 9. 모니터링 설정

### 9.1 시스템 모니터링
- Prometheus + Grafana
- API 성능 메트릭
- Sentry 에러 추적

### 9.2 로깅
- JSON 구조화 로깅
- ELK 스택 연동
- OAuth 인증 로그 추적

## 10. 배포 환경

### 10.1 인프라 구성
- AWS ECS/Fargate
- RDS (PostgreSQL)
- ElastiCache (Redis)
- S3 (이미지 저장)
- CloudFront (정적 자원)

### 10.2 CI/CD
- GitHub Actions
- Docker 컨테이너화
- Blue/Green 배포

## 11. 개발 일정

### Phase 1 (4주)
- Google OAuth 인증 구현
- 기본 API 구조 설정
- DB 스키마 구현
- Google 캘린더 연동

### Phase 2 (4주)
- LLM 통합
- 채팅 기능 구현
- OCR 처리 구현

### Phase 3 (2주)
- 테스트 및 버그 수정
- 성능 최적화
- 배포 환경 구성