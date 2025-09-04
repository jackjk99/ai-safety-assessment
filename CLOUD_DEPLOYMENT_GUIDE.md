# ☁️ 클라우드 배포 가이드 (비용 최적화)

## 🎯 배포 구성
- **Supabase**: 데이터베이스 (무료)
- **Vercel**: 프론트엔드 (무료)
- **Railway**: 백엔드 (무료)

## 📋 사전 준비사항

### 1. GitHub 저장소 준비
```bash
# 현재 변경사항 커밋
git add .
git commit -m "클라우드 배포 준비 완료"
git push origin main
```

### 2. 필요한 계정들
- [GitHub](https://github.com) 계정
- [Supabase](https://supabase.com) 계정
- [Vercel](https://vercel.com) 계정
- [Railway](https://railway.app) 계정

## 🚀 1단계: Supabase 설정

### A. 프로젝트 생성
1. [Supabase](https://supabase.com) 로그인
2. **"New Project"** 클릭
3. **Project Name**: `ai-safety-assessment`
4. **Database Password**: 안전한 비밀번호 설정
5. **Region**: `Asia Pacific (Northeast) - Tokyo`

### B. 데이터베이스 스키마 설정
**SQL Editor**에서 다음 스크립트 실행:

```sql
-- 사용자 테이블
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    organization VARCHAR(100),
    role VARCHAR(20) DEFAULT 'beta_tester',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 분석 세션 테이블
CREATE TABLE analysis_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(id),
    analysis_status VARCHAR(20) DEFAULT 'pending',
    analysis_result JSONB,
    feedback TEXT,
    feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 업로드된 이미지 테이블
CREATE TABLE uploaded_images (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES analysis_sessions(id),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 분석 파일 테이블
CREATE TABLE analysis_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(50),
    session_id UUID REFERENCES analysis_sessions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### C. 베타 테스터 계정 생성
```sql
-- 베타 테스터 계정들 생성
INSERT INTO users (username, email, full_name, organization, role) VALUES
('tester1', 'tester1@example.com', '베타 테스터 1', '테스트 조직', 'beta_tester'),
('tester2', 'tester2@example.com', '베타 테스터 2', '테스트 조직', 'beta_tester'),
('tester3', 'tester3@example.com', '베타 테스터 3', '테스트 조직', 'beta_tester');
```

### D. API 키 확인
1. **Settings** → **API** 메뉴
2. **Project URL** 복사
3. **anon public** 키 복사

## 🚀 2단계: Railway 백엔드 배포

### A. Railway 프로젝트 생성
1. [Railway](https://railway.app) 로그인
2. **"Start a New Project"** 클릭
3. **"Deploy from GitHub repo"** 선택
4. GitHub 저장소 연결

### B. 환경 변수 설정
Railway 대시보드에서 **Variables** 탭에 다음 설정:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### C. 배포 확인
1. **Deployments** 탭에서 배포 상태 확인
2. **Domains** 탭에서 생성된 URL 확인 (예: `https://your-app.railway.app`)

## 🚀 3단계: Vercel 프론트엔드 배포

### A. Vercel 프로젝트 생성
1. [Vercel](https://vercel.com) 로그인
2. **"New Project"** 클릭
3. GitHub 저장소 연결
4. **Framework Preset**: `Other`
5. **Root Directory**: `frontend`

### B. 환경 변수 설정
Vercel 대시보드에서 **Environment Variables** 설정:

```env
REACT_APP_API_URL=https://your-railway-app.railway.app
```

### C. 배포 확인
1. **Deployments** 탭에서 배포 상태 확인
2. 생성된 URL 확인 (예: `https://your-app.vercel.app`)

## 🚀 4단계: 연결 및 테스트

### A. 프론트엔드 API URL 업데이트
`frontend/app.js`에서 Railway URL로 수정:

```javascript
const API_BASE = 'https://your-railway-app.railway.app';
```

### B. 재배포
```bash
git add .
git commit -m "API URL 업데이트"
git push origin main
```

### C. 테스트
1. Vercel URL로 접속
2. 베타 테스터 계정으로 로그인
3. 이미지 업로드 및 분석 테스트

## 🔧 문제 해결

### A. CORS 오류
Railway에서 CORS 설정 확인:
```python
# main.py에서 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### B. 환경 변수 오류
Railway와 Vercel에서 환경 변수가 올바르게 설정되었는지 확인

### C. 데이터베이스 연결 오류
Supabase 프로젝트 URL과 API 키가 올바른지 확인

## 💰 비용 정보

### 무료 티어 제한
- **Supabase**: 500MB 데이터베이스, 2GB 파일 저장소
- **Vercel**: 월 100GB 대역폭
- **Railway**: 월 $5 크레딧 (무료 티어)

### 비용 최적화 팁
1. 이미지 압축으로 저장 공간 절약
2. 불필요한 로그 파일 정리
3. 사용하지 않는 기능 비활성화

## 🎉 배포 완료!

이제 외부에서도 접속 가능한 베타 서비스가 완성되었습니다!
