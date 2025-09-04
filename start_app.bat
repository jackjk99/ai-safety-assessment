@echo off
echo AI Safety Assessment App 시작...
echo.
echo 이 스크립트는 백엔드와 프론트엔드를 모두 실행합니다.
echo.
echo 주의: OpenAI API 키가 설정되어 있어야 합니다.
echo backend\.env 파일에 OPENAI_API_KEY를 설정하세요.
echo.
pause

echo.
echo 1. 백엔드 서버 시작 (새 창에서)...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate.bat && python main.py"

echo.
echo 2. 프론트엔드 서버 시작 (새 창에서)...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo 3. 브라우저에서 다음 주소로 접속:
echo    프론트엔드: http://localhost:3000
echo    백엔드 API: http://localhost:8000
echo    API 문서: http://localhost:8000/docs
echo.
echo 모든 서버가 실행되었습니다.
pause
