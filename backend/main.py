from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
import os
import base64
from PIL import Image
import io
import json
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from auth import get_auth_manager, get_current_active_user, create_beta_testers
from database import get_db_manager
from file_storage import get_file_storage_manager

# 환경변수 로드
load_dotenv()

app = FastAPI(title="AI Safety Assessment API", version="1.0.0")

# CORS 설정 (외부 접속 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 설정
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# OpenAI 클라이언트 초기화
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API 키가 설정되지 않았습니다.")
    return OpenAI(api_key=api_key)

# 기본 체크리스트 생성
def create_default_checklist():
    checklist_data = {
        "항목": [
            "모든 작업자는 작업조건에 맞는 안전보호구를 착용한다.",
            "모든 공사성 작업시에는 위험성평가를 시행하고 결과를 기록/보관한다.",
            "작업 전 반드시 TBM작업계획 공유 및 위험성 예지 등 시행",
            "고위험 작업 시에는 2인1조 작업 및 작업계획서를 비치한다.",
            "이동식사다리 및 고소작업대(차량) 사용 시 안전수칙 준수",
            "전원작업 및 고압선 주변 작업 시 감전예방 조치",
            "도로 횡단 및 도로 주변 작업 시 교통안전 시설물과 신호수를 배치한다.",
            "밀폐공간(맨홀 등) 작업 시 산소/유해가스 농도 측정 및 감시인 배치",
            "하절기/동절기 기상상황에 따른 옥외작업 금지",
            "유해위험물 MSDS의 관리 및 예방 조치",
            "중량물 이동 인력, 장비 이용 시 안전 조치",
            "화기 작업 화상, 화재 위험 예방 조치",
            "추락 예방 안전 조치",
            "건설 기계장비, 설비 등 안전 및 방호조치(끼임)",
            "혼재 작업(부딪힘) 시 안전 예방 조치",
            "충돌 방지 조치(부딪힘)"
        ]
    }
    return pd.DataFrame(checklist_data)

# 이미지를 base64로 인코딩
def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    return base64.b64encode(image_bytes).decode('utf-8')

# AI 분석 결과 파싱
def parse_analysis_sections(analysis_text: str) -> Dict:
    sections = {
        "risk_analysis": "",
        "sgr_checklist": "",
        "recommendations": ""
    }
    
    # 간단한 파싱 로직 (실제로는 더 정교한 파싱이 필요할 수 있음)
    lines = analysis_text.split('\n')
    current_section = None
    
    for line in lines:
        if "위험요인" in line or "잠재 위험" in line:
            current_section = "risk_analysis"
        elif "체크리스트" in line or "SGR" in line:
            current_section = "sgr_checklist"
        elif "권장사항" in line or "추가 권장" in line:
            current_section = "recommendations"
        
        if current_section:
            sections[current_section] += line + "\n"
    
    return sections


def _extract_first_markdown_table_block(text: str) -> List[str]:
    """주어진 텍스트에서 첫 번째 마크다운 표 블록(연속된 '|' 라인들)을 라인 리스트로 반환.
    표가 없으면 빈 리스트를 반환한다.
    """
    lines = [ln.rstrip() for ln in text.split("\n")]
    n = len(lines)
    i = 0
    while i < n:
        line = lines[i].strip()
        # 표의 헤더 라인 후보: 파이프 포함
        if line.startswith("|") and "|" in line:
            # 다음 라인이 구분선(---)인지 확인
            j = i + 1
            if j < n:
                sep = lines[j].strip()
                if set(sep.replace("|", "").replace(":", "").replace(" ", "")) <= {"-"} and "|" in sep:
                    # 표 시작 지점 확인됨. 연속된 파이프 라인 수집
                    k = j + 1
                    table_block = [lines[i], lines[j]]
                    while k < n and lines[k].strip().startswith("|"):
                        table_block.append(lines[k])
                        k += 1
                    return table_block
        i += 1
    return []


def _split_md_row(row: str) -> List[str]:
    # 양끝 파이프 제거 후 셀 분리
    core = row.strip()
    if core.startswith("|"):
        core = core[1:]
    if core.endswith("|"):
        core = core[:-1]
    cells = [c.strip() for c in core.split("|")]
    return cells


def _html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def markdown_table_to_inner_html(markdown_text: str) -> str:
    """마크다운 표를 HTML thead/tbody(inner only)로 변환. 표가 없으면 빈 문자열 반환."""
    block = _extract_first_markdown_table_block(markdown_text)
    if not block:
        return ""

    # 최소 2라인(헤더, 구분선) 필요
    if len(block) < 2:
        return ""

    header_cells = _split_md_row(block[0])
    # 구분선(block[1])은 사용하지 않음
    data_rows = [
        _split_md_row(r)
        for r in block[2:]
    ]

    # HTML 조립 (table 태그 제외)
    thead = "<thead><tr>" + "".join(f"<th>{_html_escape(h)}</th>" for h in header_cells) + "</tr></thead>"
    tbody_parts: List[str] = []
    for row in data_rows:
        tds = "".join(f"<td>{_html_escape(c)}</td>" for c in row)
        tbody_parts.append(f"<tr>{tds}</tr>")
    tbody = "<tbody>" + "".join(tbody_parts) + "</tbody>"
    return thead + tbody

# 이미지 분석 수행
async def analyze_images_with_openai(images: List[Image.Image], image_names: List[str]) -> Dict:
    client = get_openai_client()
    
    # 체크리스트 로드
    checklist_df = create_default_checklist()
    checklist_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(checklist_df['항목'])])
    
    # 프롬프트 구성
    prompt = f"""
당신은 건설현장 안전관리 전문가입니다. 제공된 {len(images)}장의 현장 사진을 분석하여 다음 형식으로 위험성 평가서를 작성해주세요.

**중요사항**: 
- 제공된 {len(images)}장의 사진은 모두 동일한 공사현장의 서로 다른 각도/영역을 촬영한 것입니다.
- 모든 사진을 종합적으로 분석하여 현장 전체의 통합된 위험성 평가를 수행해주세요.
- 각 사진별로 개별 분석하지 말고, 전체 현장의 종합적인 관점에서 분석해주세요.

## 분석 요구사항:
1. 현장 전체 잠재 위험요인 분석 및 위험성 감소대책 (표 형식)
2. SGR 체크리스트 항목별 통합 체크 결과 (표 형식)
3. 현장 전체 통합 추가 권장사항

## SGR 체크리스트 항목:
{checklist_text}

## 출력 형식: html 표 형식으로 작성하고 [현장 전체에서 식별된 모든 주요 위험요인들을 설명한다

### 1. 현장 전체 잠재 위험요인 분석 및 위험성 감소대책
| 번호 | 잠재 위험요인 | 잠재 위험요인 설명 | 위험성 감소대책 |
| 1 | [위험요인1]  | [현장 전체 관점에서의 상세 설명] | ① [대책1] ② [대책2] ③ [대책3] ④ [대책4] |
| 2 | [위험요인2]  | [현장 전체 관점에서의 상세 설명] | ① [대책1] ② [대책2] ③ [대책3] ④ [대책4] |


### 2. SGR 체크리스트 항목별 통합 체크 결과
| 항목 | 준수여부 | 세부 내용 |
|----------------|----------|-------------------|
| 1. 모든 작업자는 작업조건에 맞는 안전보호구를 착용한다. | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 2. 모든 공사성 작업시에는 위험성평가를 시행하고 결과를 기록/보관한다. | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 3. 작업 전 반드시 TBM작업계획 공유 및 위험성 예지 등 시행 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 4. 고위험 작업 시에는 2인1조 작업 및 작업계획서를 비치한다. | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 5. 이동식사다리 및 고소작업대(차량) 사용 시 안전수칙 준수 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 6. 전원작업 및 고압선 주변 작업 시 감전예방 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 7. 도로 횡단 및 도로 주변 작업 시 교통안전 시설물과 신호수를 배치한다. | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 8. 밀폐공간(맨홀 등) 작업 시 산소/유해가스 농도 측정 및 감시인 배치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 9. 하절기/동절기 기상상황에 따른 옥외작업 금지 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 10. 유해위험물 MSDS의 관리 및 예방 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 11. 중량물 이동 인력, 장비 이용 시 안전 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 12. 화기 작업 화상, 화재 위험 예방 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 13. 추락 예방 안전 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 14. 건설 기계장비, 설비 등 안전 및 방호조치(끼임) | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 15. 혼재 작업(부딪힘) 시 안전 예방 조치 | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
| 16. 충돌 방지 조치(부딪힘) | [O 또는 X 또는 해당없음 또는 알수없음] | [현장 사진들에서 확인된 구체적 상황] |
**중요** 

### 3. 현장 전체 통합 추가 권장사항
구체적이고 실용적인 권장사항을 제시해주세요.

**제약사항**
- 모든 내용은 실제 산업안전보건 기준에 부합하도록 구체적이고 실무적인 수준으로 작성
- 위험성 감소대책은 각각 4개 이상의 구체적인 조치로 구성
- 체크리스트는 현장 전체 상황에 맞게 O, X , 해당없음 , 알수없음 중 하나로 표시하고 구체적인 확인 내용도 포함
  o: 사진에서 준수가 명확히 확인됨, x: 사진에서 명확히 미준수가 확인됨, 해당없음: 준수가 필요 없는 항목임, 알수없음: 이미지의 내용으로 확인 불가한 경우
  **중요사항** 각 상태에서 대한 판단기준은 최대한 사진에서 확인되는 사항에 대해서만 O, X, 해당없음으로 표시하고 여러번 수행시에도 동일한 결과가 나오도록 해줘
   
- 모든 출력은 한국어로 작성
- 실무에서 바로 활용 가능한 수준의 상세한 내용 포함
- 개별 사진 분석이 아닌 현장 전체의 통합적 관점에서 분석

분석 대상 이미지: {', '.join(image_names)}
총 이미지 수: {len(images)}장
"""
    
    # 이미지들을 base64로 인코딩
    image_contents = []
    for image in images:
        base64_image = encode_image_to_base64(image)
        image_contents.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    # OpenAI API 호출
    try:
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        print(f"🤖 OpenAI API 호출 시작 - 모델: {model_name}")
        print(f"📝 프롬프트 길이: {len(prompt)} 문자")
        print(f"🖼️ 이미지 수: {len(image_contents)}장")
        
        response = client.chat.completions.create(
            model=model_name,  # 환경변수에서 가져온 모델명 사용
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *image_contents
                    ]
                }
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        print(f"✅ OpenAI API 응답 성공")
        
        analysis_result = response.choices[0].message.content
        
        # 결과 파싱 및 표 변환
        sections_raw = parse_analysis_sections(analysis_result)
        sections = {
            "risk_analysis": markdown_table_to_inner_html(sections_raw.get("risk_analysis", "")),
            "sgr_checklist": markdown_table_to_inner_html(sections_raw.get("sgr_checklist", "")),
            "recommendations": sections_raw.get("recommendations", "")
        }
        
        return {
            "image_names": image_names,
            "image_count": len(images),
            "full_report": analysis_result,
            "sections": sections,
            "timestamp": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API 호출 중 오류 발생: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """메인 페이지"""
    # 프론트엔드 HTML 파일 경로 수정
    html_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # 파일을 찾을 수 없는 경우 간단한 HTML 반환
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head><title>AI Safety Assessment</title></head>
        <body>
            <h1>AI Safety Assessment API</h1>
            <p>프론트엔드 파일을 찾을 수 없습니다. <a href="/docs">API 문서</a>를 확인하세요.</p>
        </body>
        </html>
        """)

@app.post("/analyze")
async def analyze_images(
    files: List[UploadFile] = File(...),
    session_name: str = Form("분석 세션"),
    current_user: dict = Depends(get_current_active_user)
):
    """이미지 분석 API (인증 필요)"""
    if not files:
        raise HTTPException(status_code=400, detail="업로드된 파일이 없습니다.")
    
    try:
        # 데이터베이스 및 파일 저장 매니저 초기화
        db_manager = get_db_manager()
        file_storage = get_file_storage_manager()
        
        # 분석 세션 생성
        session = await db_manager.create_analysis_session(
            user_id=current_user["id"],
            session_name=session_name,
            image_count=len(files)
        )
        session_id = session["id"]
        
        # 이미지 파일들 저장
        saved_images = await file_storage.save_uploaded_images(
            session_id=session_id,
            user_id=current_user["id"],
            files=files
        )
        
        # 이미지 로드 및 분석 준비
        images = []
        image_names = []
        
        for file in files:
            if not file.content_type.startswith('image/'):
                continue
                
            try:
                # 이미지 로드 (file.file을 직접 사용)
                image = Image.open(file.file)
                
                # 이미지 크기 조정 (API 제한 고려)
                max_size = 1024
                if max(image.size) > max_size:
                    ratio = max_size / max(image.size)
                    new_size = tuple(int(dim * ratio) for dim in image.size)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                
                images.append(image)
                image_names.append(file.filename)
                print(f"이미지 로드 성공: {file.filename}, 크기: {image.size}")
                
            except Exception as img_error:
                print(f"이미지 로드 실패: {file.filename}, 오류: {img_error}")
                continue
        
        if not images:
            raise HTTPException(status_code=400, detail="유효한 이미지 파일이 없습니다.")
        
        # AI 분석 수행
        print(f"🔍 AI 분석 시작: {len(images)}장의 이미지")
        result = await analyze_images_with_openai(images, image_names)
        print(f"✅ AI 분석 완료: {result.get('timestamp', 'N/A')}")
        
        # 분석 결과에 세션 정보 추가
        result["session_id"] = session_id
        result["user_id"] = current_user["id"]
        
        # 분석 결과 파일들 저장
        await file_storage.save_analysis_results(
            session_id=session_id,
            user_id=current_user["id"],
            analysis_result=result
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류 발생: {str(e)}")

# 인증 관련 API 엔드포인트들
@app.post("/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """사용자 로그인"""
    auth_manager = get_auth_manager()
    user = await auth_manager.authenticate_user(username, password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="잘못된 사용자명 또는 비밀번호입니다."
        )
    
    access_token = auth_manager.create_access_token(
        data={"sub": user["username"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "full_name": user.get("full_name"),
            "organization": user.get("organization")
        }
    }

@app.post("/auth/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(None),
    organization: str = Form(None)
):
    """새 사용자 등록 (베타 테스트용)"""
    auth_manager = get_auth_manager()
    
    try:
        user = await auth_manager.register_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            organization=organization
        )
        
        return {
            "message": "사용자 등록이 완료되었습니다.",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 등록 중 오류: {str(e)}")

@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """현재 사용자 정보 조회"""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user.get("full_name"),
        "organization": current_user.get("organization"),
        "role": current_user.get("role", "beta_tester")
    }

@app.get("/auth/sessions")
async def get_user_sessions(current_user: dict = Depends(get_current_active_user)):
    """사용자의 분석 세션 목록 조회"""
    file_storage = get_file_storage_manager()
    sessions = await file_storage.get_user_files(current_user["id"])
    return sessions

# 피드백 관련 API
@app.post("/feedback/{session_id}")
async def submit_feedback(
    session_id: str,
    feedback: str = Form(...),
    rating: int = Form(...),
    current_user: dict = Depends(get_current_active_user)
):
    """분석 세션에 대한 피드백 제출"""
    if not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="평점은 1-5 사이여야 합니다.")
    
    db_manager = get_db_manager()
    
    try:
        await db_manager.save_feedback(session_id, feedback, rating)
        return {"message": "피드백이 성공적으로 저장되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"피드백 저장 중 오류: {str(e)}")

@app.get("/styles.css")
async def get_styles():
    """CSS 파일 서빙"""
    css_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "styles.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content, media_type="text/css")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/app.js")
async def get_app_js():
    """JavaScript 파일 서빙"""
    js_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "app.js")
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content, media_type="application/javascript")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JavaScript file not found")

@app.get("/health")
async def health_check():
    """헬스 체크"""
    seoul_tz = timezone(timedelta(hours=9))
    seoul_time = datetime.now(seoul_tz)
    return {"status": "healthy", "timestamp": seoul_time.isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
