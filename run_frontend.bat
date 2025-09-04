@echo off
echo AI Safety Assessment Frontend 실행 중...
echo.
echo Python HTTP 서버 시작...
cd frontend
python -m http.server 3000

echo.
echo 프론트엔드가 http://localhost:3000 에서 실행 중입니다.
echo 백엔드도 별도로 실행해야 합니다.
pause
