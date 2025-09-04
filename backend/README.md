# AI Safety Assessment Backend

실제 OpenAI API를 연동한 AI 위험성평가 백엔드 서버입니다.

## 🚀 기능

- **실제 AI 분석**: OpenAI GPT-4 Vision API를 사용한 실제 이미지 분석
- **다중 이미지 처리**: 여러 이미지를 동시에 업로드하여 통합 분석
- **SGR 체크리스트**: 산업안전보건기준에 따른 체크리스트 자동 검증
- **위험요인 분석**: 현장의 잠재 위험요인 식별 및 대책 제시
- **RESTful API**: FastAPI 기반의 현대적인 웹 API

## 📋 요구사항

- Python 3.8 이상
- OpenAI API 키
- 인터넷 연결

## 🛠️ 설치 및 설정

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate.bat

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# .env 파일 생성
cp env_example.txt .env
```

`.env` 파일 내용:
```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here

# OpenAI 모델 설정 (기본값: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# 서버 설정
HOST=0.0.0.0
PORT=8000
```

### 4. OpenAI API 키 발급

1. [OpenAI 웹사이트](https://platform.openai.com/)에 가입
2. API 키 발급
3. `.env` 파일에 API 키 입력

## 🚀 서버 실행

### 개발 모드
```bash
python main.py
```

### 프로덕션 모드
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 다음 URL에서 접근할 수 있습니다:
- **API 문서**: http://localhost:8000/docs
- **메인 페이지**: http://localhost:8000/
- **헬스 체크**: http://localhost:8000/health

## 📡 API 엔드포인트

### POST /analyze
이미지 분석을 수행합니다.

**요청:**
- Content-Type: `multipart/form-data`
- Body: `files` (이미지 파일들)

**응답:**
```json
{
  "image_names": ["image1.jpg", "image2.jpg"],
  "image_count": 2,
  "full_report": "전체 분석 보고서...",
  "sections": {
    "risk_analysis": "위험요인 분석 테이블...",
    "sgr_checklist": "체크리스트 결과 테이블...",
    "recommendations": "권장사항..."
  },
  "timestamp": "2024-01-01 12:00:00"
}
```

### GET /health
서버 상태를 확인합니다.

**응답:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🔧 설정 옵션

### OpenAI 모델 선택
`.env` 파일에서 사용할 모델을 변경할 수 있습니다:

```env
# GPT-4 Vision (고품질, 높은 비용)
OPENAI_MODEL=gpt-4o

# GPT-4o-mini (균형, 적당한 비용)
OPENAI_MODEL=gpt-4o-mini

# GPT-4 Vision (이전 버전)
OPENAI_MODEL=gpt-4-vision-preview
```

### 이미지 크기 제한
`main.py`에서 이미지 크기 제한을 조정할 수 있습니다:

```python
# 이미지 크기 조정 (API 제한 고려)
max_size = 1024  # 최대 픽셀 크기
```

## 📊 분석 결과 형식

### 위험요인 분석
| 번호 | 잠재 위험요인 | 잠재 위험요인 설명 | 위험성 감소대책 |

### SGR 체크리스트
| 항목 | 준수여부 | 세부 내용 |

### 권장사항
구체적이고 실용적인 현장 개선 권장사항

## 🐛 문제 해결

### 일반적인 오류

1. **OpenAI API 키 오류**
   ```
   OpenAI API 키가 설정되지 않았습니다.
   ```
   - `.env` 파일에 올바른 API 키가 설정되어 있는지 확인
   - API 키가 유효한지 확인

2. **이미지 업로드 오류**
   ```
   유효한 이미지 파일이 없습니다.
   ```
   - 지원되는 이미지 형식: JPEG, PNG, GIF, WebP
   - 파일 크기가 너무 크지 않은지 확인

3. **서버 연결 오류**
   ```
   백엔드 서버에 연결할 수 없습니다.
   ```
   - 서버가 실행 중인지 확인
   - 포트 8000이 사용 가능한지 확인
   - 방화벽 설정 확인

### 로그 확인

서버 실행 시 상세한 로그를 확인할 수 있습니다:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## 🔒 보안 고려사항

1. **API 키 보호**: `.env` 파일을 `.gitignore`에 추가
2. **CORS 설정**: 프로덕션 환경에서는 특정 도메인만 허용
3. **파일 크기 제한**: 업로드 파일 크기 제한 설정
4. **요청 제한**: API 호출 빈도 제한 고려

## 📈 성능 최적화

1. **이미지 압축**: 업로드 전 이미지 크기 조정
2. **캐싱**: 동일한 이미지에 대한 결과 캐싱
3. **비동기 처리**: 대용량 파일 처리 시 비동기 처리
4. **로드 밸런싱**: 트래픽이 많을 때 로드 밸런서 사용

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.
