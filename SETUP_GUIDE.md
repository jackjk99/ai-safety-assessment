# AI Safety Assessment App 설정 가이드

## 🚀 빠른 시작

### 1. 환경 설정
1. **OpenAI API 키 발급**
   - [OpenAI 웹사이트](https://platform.openai.com/)에서 API 키 발급
   - `backend\.env` 파일 생성 (env_example.txt 복사)
   - `OPENAI_API_KEY=your_actual_api_key` 설정

2. **Python 가상환경 설정**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate.ps1
   pip install -r requirements.txt
   ```

### 2. 실행 방법

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
venv\Scripts\activate.bat
python main.py

# 프론트엔드 (새 터미널에서)
cd frontend
python -m http.server 3000
```

### 3. 접속 주소
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 🔧 문제 해결

### 일반적인 오류
1. **포트 충돌**: 8000번 또는 3000번 포트가 사용 중인 경우
2. **가상환경 문제**: `venv\Scripts\activate.ps1` 실행 후 pip install
3. **API 키 오류**: `.env` 파일에 올바른 API 키 설정

### 로그 확인
- 백엔드: 터미널에서 오류 메시지 확인
- 프론트엔드: 브라우저 개발자 도구 콘솔 확인

## 📱 사용법
1. 브라우저에서 http://localhost:3000 접속
2. 현장 사진 여러 장 업로드
3. "통합 분석" 버튼 클릭
4. AI 분석 결과 확인 및 체크리스트 다운로드

## 🆘 지원
문제가 발생하면 다음을 확인하세요:
1. 모든 의존성이 설치되었는지
2. OpenAI API 키가 올바른지
3. 포트가 사용 가능한지
4. 가상환경이 활성화되었는지
