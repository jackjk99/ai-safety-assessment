@echo off
echo AI Safety Assessment Backend 실행 중...
echo.
echo 1. 가상환경 활성화...
call backend\venv\Scripts\activate.bat

echo.
echo 2. 의존성 설치 확인...
pip install -r backend\requirements.txt

echo.
echo 3. 백엔드 서버 시작...
cd backend
python main.py

pause
