# Railway 환경 변수 설정 가이드

## 🚨 필수 환경 변수 설정

Railway에서 애플리케이션이 정상적으로 실행되려면 다음 환경 변수들을 반드시 설정해야 합니다.

### **1. Railway 대시보드 접속**
1. [Railway.app](https://railway.app) 로그인
2. 프로젝트 선택
3. **Variables** 탭 클릭

### **2. 필수 환경 변수 추가**

각 변수를 **New Variable** 버튼으로 추가:

| 변수명 | 값 | 설명 |
|--------|-----|------|
| `OPENAI_API_KEY` | `sk-...` | OpenAI API 키 (sk-로 시작) |
| `OPENAI_MODEL` | `gpt-4o-mini` | 사용할 OpenAI 모델 |
| `SUPABASE_URL` | `https://[프로젝트ID].supabase.co` | Supabase 프로젝트 URL |
| `SUPABASE_KEY` | `[anon public 키]` | Supabase 익명 키 |
| `SECRET_KEY` | `[service role 키]` | JWT 토큰 암호화 키 |
| `ALGORITHM` | `HS256` | JWT 알고리즘 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | 토큰 만료 시간 |

### **3. 환경 변수 값 확인 방법**

#### **OpenAI API 키**
- [OpenAI Platform](https://platform.openai.com/api-keys)에서 확인
- `sk-`로 시작하는 키

#### **Supabase 설정**
- Supabase 프로젝트 대시보드 → **Settings** → **API**
- **Project URL**: `https://[프로젝트ID].supabase.co`
- **anon public**: `[anon public 키]` (eyJ...로 시작)
- **service_role secret**: `[service role 키]` (eyJ...로 시작)

#### **JWT Secret Key**
- 임의의 긴 문자열 (예: `my-super-secret-jwt-key-2024`)

### **4. 설정 완료 후**

1. **Deployments** 탭에서 새로운 배포 확인
2. **Logs** 탭에서 서버 시작 로그 확인
3. **헬스체크 성공** 확인

### **5. 문제 해결**

**환경 변수 설정 후에도 문제가 있다면:**
- Railway 로그에서 오류 메시지 확인
- 환경 변수 이름과 값이 정확한지 확인
- Supabase 연결 테스트

---

## 📝 예시 환경 변수

```
OPENAI_API_KEY=sk-proj-abc123def456ghi789
OPENAI_MODEL=gpt-4o-mini
SUPABASE_URL=https://[프로젝트ID].supabase.co
SUPABASE_KEY=[anon public 키]
SECRET_KEY=[service role 키]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ 주의:** 실제 API 키는 절대 공개하지 마세요!
