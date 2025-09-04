# AI Safety Assessment App - 베타 테스트 설정 가이드

## 🚀 빠른 시작

### 1. 환경 설정
1. **OpenAI API 키 발급**
   - [OpenAI 웹사이트](https://platform.openai.com/)에서 API 키 발급
   - `backend\.env` 파일 생성 (env_example.txt 복사)
   - `OPENAI_API_KEY=your_actual_api_key` 설정

2. **Supabase 데이터베이스 설정**
   - [Supabase 웹사이트](https://supabase.com/)에서 새 프로젝트 생성
   - 프로젝트 URL과 anon key 복사
   - `.env` 파일에 추가:
     ```
     SUPABASE_URL=your_supabase_project_url
     SUPABASE_ANON_KEY=your_supabase_anon_key
     SECRET_KEY=your_random_secret_key
     ```

3. **Python 가상환경 설정**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate.ps1
   pip install -r requirements.txt
   ```

### 2. 데이터베이스 초기화
1. **Supabase 대시보드에서 테이블 생성**
   - Supabase 프로젝트 대시보드 → SQL Editor
   - `backend/database.py`의 `create_tables()` 함수에서 출력되는 SQL 실행

2. **베타 테스터 계정 생성**
   ```bash
   cd backend
   python init_beta_testers.py
   ```

### 3. 실행 방법

#### 방법 1: 통합 실행 (권장)
```bash
start_app.bat
```

#### 방법 2: 개별 실행
```bash
# 백엔드 실행
run_backend.bat

# 프론트엔드 실행 (새 터미널에서)
run_frontend.bat
```

#### 방법 3: 수동 실행
```bash
# 백엔드
cd backend
venv\Scripts\activate.ps1
python main.py

# 프론트엔드 (새 터미널에서)
cd frontend
python -m http.server 3000
```

### 4. 접속 주소
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 🔐 베타 테스터 계정

### 기본 계정
- **tester1** / beta123! (건설회사 A)
- **tester2** / beta123! (안전관리업체 B)  
- **tester3** / beta123! (건설회사 C)

### 새 계정 등록
- 웹 인터페이스에서 직접 등록 가능
- 또는 API를 통해 관리자 권한으로 추가

## 📱 베타 테스트 사용법

### 1. 로그인
- 웹사이트 접속 시 자동으로 로그인 모달 표시
- 베타 테스터 계정으로 로그인

### 2. 이미지 분석
1. 현장 사진 여러 장 업로드
2. "통합 분석" 버튼 클릭
3. AI 분석 결과 확인

### 3. 피드백 제출
1. 분석 완료 후 "피드백" 탭 클릭
2. 만족도 평가 (1-5점)
3. 상세 피드백 작성
4. "피드백 제출" 버튼 클릭

## 🔧 문제 해결

### 일반적인 오류
1. **Supabase 연결 오류**
   - `.env` 파일의 SUPABASE_URL, SUPABASE_ANON_KEY 확인
   - Supabase 프로젝트가 활성화되어 있는지 확인

2. **인증 오류**
   - 베타 테스터 계정이 올바르게 생성되었는지 확인
   - `python init_beta_testers.py` 재실행

3. **포트 충돌**
   - 8000번 또는 3000번 포트가 사용 중인 경우
   - 다른 포트로 변경하거나 기존 프로세스 종료

### 로그 확인
- 백엔드: 터미널에서 오류 메시지 확인
- 프론트엔드: 브라우저 개발자 도구 콘솔 확인

## 📊 베타 테스트 데이터 수집

### 자동 수집 데이터
- 사용자별 분석 세션 기록
- 업로드된 이미지 파일
- AI 분석 결과
- 피드백 및 평점

### 데이터 확인 방법
- Supabase 대시보드에서 실시간 데이터 확인
- 각 테이블별로 사용자 활동 모니터링

## 🌐 외부 접속 설정

### 1. 방화벽 설정
- 포트 8000, 3000 열기
- 보안 그룹 설정 (AWS, GCP 등)

### 2. 도메인 설정 (선택사항)
- 도메인 구매 및 DNS 설정
- SSL 인증서 설치

### 3. 프로덕션 배포
- Docker 컨테이너화
- Nginx 리버스 프록시
- PM2 프로세스 관리

## 🆘 지원

문제가 발생하면 다음을 확인하세요:
1. 모든 의존성이 설치되었는지
2. OpenAI API 키가 올바른지
3. Supabase 설정이 완료되었는지
4. 포트가 사용 가능한지
5. 가상환경이 활성화되었는지

## 📈 베타 테스트 완료 후

### 데이터 분석
- 사용자 피드백 분석
- 분석 정확도 평가
- 사용성 개선사항 도출

### 서비스 개선
- 피드백 기반 기능 개선
- UI/UX 최적화
- 성능 최적화

### 정식 출시 준비
- 보안 강화
- 확장성 개선
- 모니터링 시스템 구축
