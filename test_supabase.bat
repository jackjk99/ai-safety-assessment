@echo off
echo ========================================
echo    Supabase 연동 테스트 시작
echo ========================================
echo.

cd backend

echo 1. 환경 변수 확인...
python check_env.py
echo.

echo 2. 간단한 Supabase 연결 테스트...
python test_supabase_simple.py
echo.

echo 3. 상세 Supabase 연동 테스트...
python test_supabase_detailed.py
echo.

echo ========================================
echo    테스트 완료
echo ========================================
echo.
echo 결과를 확인하고 문제가 있으면 SUPABASE_TEST_GUIDE.md를 참조하세요.
echo.
pause
