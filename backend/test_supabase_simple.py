#!/usr/bin/env python3
"""
Supabase 간단 연동 테스트 스크립트
"""
import os
import sys
from dotenv import load_dotenv

def test_supabase_connection():
    print("=== Supabase 연동 테스트 ===")
    
    # 1. 환경 변수 확인
    print("\n1. 환경 변수 확인")
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url:
        print("❌ SUPABASE_URL이 설정되지 않았습니다.")
        print("   .env 파일에 SUPABASE_URL을 설정하거나 환경 변수로 설정하세요.")
        return False
    
    if not supabase_key:
        print("❌ SUPABASE_ANON_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 SUPABASE_ANON_KEY를 설정하거나 환경 변수로 설정하세요.")
        return False
    
    print(f"✅ SUPABASE_URL: {supabase_url}")
    print(f"✅ SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    
    # 2. Supabase 라이브러리 설치 확인
    print("\n2. Supabase 라이브러리 확인")
    try:
        from supabase import create_client, Client
        print("✅ supabase 라이브러리 설치됨")
    except ImportError:
        print("❌ supabase 라이브러리가 설치되지 않았습니다.")
        print("   pip install supabase 명령으로 설치하세요.")
        return False
    
    # 3. Supabase 클라이언트 생성 테스트
    print("\n3. Supabase 클라이언트 생성 테스트")
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase 클라이언트 생성 성공")
    except Exception as e:
        print(f"❌ Supabase 클라이언트 생성 실패: {str(e)}")
        return False
    
    # 4. 기본 연결 테스트
    print("\n4. 기본 연결 테스트")
    try:
        # 간단한 API 호출 테스트
        response = supabase.table('users').select('*').limit(1).execute()
        print("✅ Supabase 연결 성공")
        print(f"   응답 데이터: {len(response.data)}개 행")
        return True
    except Exception as e:
        print(f"❌ Supabase 연결 실패: {str(e)}")
        return False

def create_env_template():
    """환경 변수 템플릿 생성"""
    print("\n=== .env 파일 템플릿 생성 ===")
    
    env_content = """# Supabase 설정
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# 기타 설정
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        print(f"⚠️  .env 파일이 이미 존재합니다: {env_path}")
        return
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ .env 파일이 생성되었습니다: {env_path}")
        print("   Supabase 프로젝트 정보를 입력한 후 다시 테스트하세요.")
    except Exception as e:
        print(f"❌ .env 파일 생성 실패: {str(e)}")

if __name__ == "__main__":
    print("Supabase 연동 테스트를 시작합니다...")
    
    # 환경 변수 파일이 없으면 템플릿 생성
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '.env')):
        create_env_template()
        print("\n환경 변수를 설정한 후 다시 실행하세요.")
        sys.exit(1)
    
    # Supabase 연동 테스트 실행
    success = test_supabase_connection()
    
    if success:
        print("\n🎉 Supabase 연동 테스트 성공!")
    else:
        print("\n❌ Supabase 연동 테스트 실패")
        print("   환경 변수 설정과 Supabase 프로젝트 설정을 확인하세요.")
