@echo off
echo ========================================
echo        베타 테스트 실행
echo ========================================
echo.

cd backend

echo 🚀 베타 테스트를 시작합니다...
echo.

echo 📡 1. Supabase 연동 테스트...
python test_supabase_simple.py
echo.

echo 👥 2. 베타 테스터 계정 생성 테스트...
python beta_test_runner.py
echo.

echo 🌐 3. 웹 애플리케이션 테스트...
python web_app_test.py
echo.

echo ========================================
echo        베타 테스트 완료
echo ========================================
echo.
echo 📋 테스트 결과를 확인하고 문제가 있으면 수정하세요.
echo.
echo 🚀 실제 애플리케이션을 시작하려면:
echo    - 백엔드: cd backend ^& python main.py
echo    - 프론트엔드: cd frontend ^& python -m http.server 3000
echo.
pause
