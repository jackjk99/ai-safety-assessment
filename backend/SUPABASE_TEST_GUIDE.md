# Supabase 연동 테스트 가이드

이 문서는 Supabase와의 연동을 테스트하는 방법을 설명합니다.

## 📋 사전 요구사항

1. **Supabase 프로젝트 생성**
   - [Supabase](https://supabase.com)에서 새 프로젝트 생성
   - 프로젝트 URL과 API 키 확인

2. **Python 환경 설정**
   - Python 3.8+ 설치
   - 가상환경 활성화: `venv\Scripts\activate` (Windows)

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 환경 변수 설정

### 1. .env 파일 생성

`backend` 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# Supabase 설정
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# 기타 설정
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Supabase 프로젝트 정보 확인

1. Supabase 대시보드에서 프로젝트 선택
2. Settings > API 메뉴로 이동
3. Project URL과 anon public key 복사

## 🧪 테스트 실행

### 1. 간단한 연결 테스트

```bash
cd backend
python test_supabase_simple.py
```

이 테스트는:
- 환경 변수 확인
- Supabase 라이브러리 설치 확인
- 기본 연결 테스트
- 클라이언트 생성 테스트

### 2. 상세 연동 테스트

```bash
cd backend
python test_supabase_detailed.py
```

이 테스트는:
- Supabase 상세 연결 테스트
- 데이터베이스 작업 테스트
- 인증 작업 테스트
- 파일 저장소 테스트

### 3. 기존 테스트 스크립트

```bash
# 환경 변수 확인
python check_env.py

# 기본 Supabase 연결 테스트
python test_supabase_connection.py

# 데이터베이스 테스트
python simple_db_test.py
```

## 📊 테스트 결과 해석

### ✅ 성공 시나리오

```
🎉 Supabase 연동 테스트 성공!
✅ SUPABASE_URL: https://xxx.supabase.co
✅ SUPABASE_ANON_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✅ supabase 라이브러리 설치됨
✅ Supabase 클라이언트 생성 성공
✅ Supabase 연결 성공
```

### ❌ 실패 시나리오

#### 환경 변수 오류
```
❌ SUPABASE_URL이 설정되지 않았습니다.
   .env 파일에 SUPABASE_URL을 설정하거나 환경 변수로 설정하세요.
```

**해결 방법:**
- `.env` 파일이 올바른 위치에 있는지 확인
- 환경 변수 이름이 정확한지 확인
- 파일 인코딩이 UTF-8인지 확인

#### 연결 오류
```
❌ Supabase 연결 실패: 401 Unauthorized
```

**해결 방법:**
- API 키가 올바른지 확인
- 프로젝트 URL이 정확한지 확인
- Supabase 프로젝트가 활성화되어 있는지 확인

#### 라이브러리 오류
```
❌ supabase 라이브러리가 설치되지 않았습니다.
   pip install supabase 명령으로 설치하세요.
```

**해결 방법:**
```bash
pip install supabase
```

## 🗄️ 데이터베이스 테이블 설정

테스트 실행 후 다음 SQL 명령어를 Supabase 대시보드의 SQL Editor에서 실행하세요:

```sql
-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    organization VARCHAR(100),
    role VARCHAR(20) DEFAULT 'beta_tester',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 분석 세션 테이블
CREATE TABLE IF NOT EXISTS analysis_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_name VARCHAR(200),
    image_count INTEGER NOT NULL,
    analysis_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    analysis_result JSONB,
    feedback TEXT,
    feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5)
);

-- 업로드된 이미지 테이블
CREATE TABLE IF NOT EXISTS uploaded_images (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 분석 결과 파일 테이블
CREATE TABLE IF NOT EXISTS analysis_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔍 문제 해결

### 일반적인 문제들

1. **환경 변수 로드 실패**
   - `.env` 파일이 `backend` 디렉토리에 있는지 확인
   - 파일 이름이 정확히 `.env`인지 확인 (확장자 없음)

2. **권한 오류**
   - Supabase 프로젝트의 RLS(Row Level Security) 설정 확인
   - API 키의 권한 설정 확인

3. **네트워크 오류**
   - 방화벽 설정 확인
   - 프록시 설정 확인

### 디버깅 팁

1. **로그 확인**
   - Python 오류 메시지 자세히 읽기
   - Supabase 대시보드의 로그 확인

2. **단계별 테스트**
   - 간단한 테스트부터 시작
   - 각 단계별로 결과 확인

3. **환경 변수 출력**
   ```python
   import os
   print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
   print(f"SUPABASE_ANON_KEY: {os.getenv('SUPABASE_ANON_KEY')}")
   ```

## 📞 지원

문제가 지속되면:
1. Supabase 프로젝트 설정 재확인
2. Python 환경 및 의존성 재설치
3. 네트워크 연결 상태 확인
4. Supabase 공식 문서 참조: [https://supabase.com/docs](https://supabase.com/docs)
