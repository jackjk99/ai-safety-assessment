#!/usr/bin/env python3
"""
베타 테스트 설정 확인 스크립트
"""

import os
import sys

def test_imports():
    """필요한 모듈들이 정상적으로 import되는지 확인"""
    print("🔍 모듈 import 테스트...")
    
    try:
        import fastapi
        print("✅ FastAPI 정상")
    except ImportError as e:
        print(f"❌ FastAPI 오류: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn 정상")
    except ImportError as e:
        print(f"❌ Uvicorn 오류: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI 정상")
    except ImportError as e:
        print(f"❌ OpenAI 오류: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas 정상")
    except ImportError as e:
        print(f"❌ Pandas 오류: {e}")
        return False
    
    try:
        import supabase
        print("✅ Supabase 정상")
    except ImportError as e:
        print(f"❌ Supabase 오류: {e}")
        return False
    
    try:
        import aiofiles
        print("✅ Aiofiles 정상")
    except ImportError as e:
        print(f"❌ Aiofiles 오류: {e}")
        return False
    
    return True

def test_environment():
    """환경변수 설정 확인"""
    print("\n🔧 환경변수 설정 확인...")
    
    # OpenAI API 키 확인
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API 키 설정됨")
    else:
        print("⚠️ OpenAI API 키가 설정되지 않음")
    
    # Supabase 설정 확인
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if supabase_url and supabase_url != "https://your-project.supabase.co":
        print("✅ Supabase URL 설정됨")
    else:
        print("⚠️ Supabase URL이 설정되지 않음")
    
    if supabase_key and supabase_key != "your_supabase_anon_key_here":
        print("✅ Supabase API 키 설정됨")
    else:
        print("⚠️ Supabase API 키가 설정되지 않음")
    
    # SECRET_KEY 확인
    secret_key = os.getenv("SECRET_KEY")
    if secret_key and secret_key != "beta_test_secret_key_12345":
        print("✅ SECRET_KEY 설정됨")
    else:
        print("⚠️ SECRET_KEY가 기본값으로 설정됨")

def main():
    """메인 함수"""
    print("🚀 AI Safety Assessment App - 베타 테스트 설정 확인")
    print("=" * 60)
    
    # 모듈 import 테스트
    if not test_imports():
        print("\n❌ 일부 모듈이 정상적으로 설치되지 않았습니다.")
        print("다음 명령을 실행하세요: pip install -r requirements.txt")
        return
    
    # 환경변수 테스트
    test_environment()
    
    print("\n" + "=" * 60)
    print("📋 다음 단계:")
    print("1. .env 파일을 생성하고 필요한 API 키들을 설정하세요")
    print("2. Supabase 프로젝트를 생성하고 데이터베이스 테이블을 만드세요")
    print("3. python main.py로 서버를 시작하세요")
    print("\n💡 베타 테스트 계정:")
    print("   - tester1 / beta123!")
    print("   - tester2 / beta123!")
    print("   - tester3 / beta123!")

if __name__ == "__main__":
    main()
