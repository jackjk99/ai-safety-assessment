#!/usr/bin/env python3
"""
Supabase 상세 연동 테스트 스크립트
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

async def test_database_operations():
    """데이터베이스 작업 테스트"""
    print("\n=== 데이터베이스 작업 테스트 ===")
    
    try:
        from database import DatabaseManager, get_db_manager
        
        # 데이터베이스 매니저 생성
        db_manager = get_db_manager()
        print("✅ DatabaseManager 생성 성공")
        
        # 테이블 생성 SQL 출력
        print("\n--- 테이블 생성 SQL ---")
        await db_manager.create_tables()
        
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 작업 테스트 실패: {str(e)}")
        return False

async def test_auth_operations():
    """인증 작업 테스트"""
    print("\n=== 인증 작업 테스트 ===")
    
    try:
        from auth import AuthManager
        
        # AuthManager 생성
        auth_manager = AuthManager()
        print("✅ AuthManager 생성 성공")
        
        # 테스트 사용자 정보
        test_user = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password_123'
        }
        
        # 사용자 등록 테스트
        print("\n--- 사용자 등록 테스트 ---")
        try:
            user = await auth_manager.register_user(
                test_user['username'],
                test_user['email'],
                test_user['password']
            )
            print(f"✅ 사용자 등록 성공: {user['username']}")
        except Exception as e:
            print(f"⚠️  사용자 등록 실패 (이미 존재할 수 있음): {str(e)}")
        
        # 로그인 테스트
        print("\n--- 로그인 테스트 ---")
        try:
            login_result = await auth_manager.authenticate_user(
                test_user['username'],
                test_user['password']
            )
            print("✅ 로그인 성공")
            print(f"   토큰: {login_result['access_token'][:20]}...")
        except Exception as e:
            print(f"❌ 로그인 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 인증 작업 테스트 실패: {str(e)}")
        return False

async def test_file_storage():
    """파일 저장소 테스트"""
    print("\n=== 파일 저장소 테스트 ===")
    
    try:
        from file_storage import FileStorageManager
        
        # FileStorageManager 생성
        storage_manager = FileStorageManager()
        print("✅ FileStorageManager 생성 성공")
        
        # 업로드 디렉토리 확인
        upload_dir = storage_manager.upload_dir
        print(f"업로드 디렉토리: {upload_dir}")
        
        if os.path.exists(upload_dir):
            print("✅ 업로드 디렉토리 존재")
        else:
            print("⚠️  업로드 디렉토리가 존재하지 않음")
        
        return True
        
    except Exception as e:
        print(f"❌ 파일 저장소 테스트 실패: {str(e)}")
        return False

async def test_supabase_connection_detailed():
    """Supabase 상세 연결 테스트"""
    print("\n=== Supabase 상세 연결 테스트 ===")
    
    try:
        from supabase import create_client, Client
        
        # 환경 변수 로드
        load_dotenv()
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ 환경 변수가 설정되지 않음")
            return False
        
        # Supabase 클라이언트 생성
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase 클라이언트 생성 성공")
        
        # 1. 사용자 테이블 테스트
        print("\n--- users 테이블 테스트 ---")
        try:
            response = supabase.table('users').select('*').limit(5).execute()
            print(f"✅ users 테이블 접근 성공: {len(response.data)}개 행")
        except Exception as e:
            print(f"❌ users 테이블 접근 실패: {str(e)}")
        
        # 2. 분석 세션 테이블 테스트
        print("\n--- analysis_sessions 테이블 테스트 ---")
        try:
            response = supabase.table('analysis_sessions').select('*').limit(5).execute()
            print(f"✅ analysis_sessions 테이블 접근 성공: {len(response.data)}개 행")
        except Exception as e:
            print(f"❌ analysis_sessions 테이블 접근 실패: {str(e)}")
        
        # 3. 업로드된 이미지 테이블 테스트
        print("\n--- uploaded_images 테이블 테스트 ---")
        try:
            response = supabase.table('uploaded_images').select('*').limit(5).execute()
            print(f"✅ uploaded_images 테이블 접근 성공: {len(response.data)}개 행")
        except Exception as e:
            print(f"❌ uploaded_images 테이블 접근 실패: {str(e)}")
        
        # 4. 분석 파일 테이블 테스트
        print("\n--- analysis_files 테이블 테스트 ---")
        try:
            response = supabase.table('analysis_files').select('*').limit(5).execute()
            print(f"✅ analysis_files 테이블 접근 성공: {len(response.data)}개 행")
        except Exception as e:
            print(f"❌ analysis_files 테이블 접근 실패: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase 상세 연결 테스트 실패: {str(e)}")
        return False

async def main():
    """메인 테스트 함수"""
    print("🚀 Supabase 상세 연동 테스트를 시작합니다...")
    
    # 환경 변수 확인
    load_dotenv()
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ 환경 변수가 설정되지 않았습니다.")
        print("   .env 파일에 SUPABASE_URL과 SUPABASE_ANON_KEY를 설정하세요.")
        return
    
    print(f"✅ 환경 변수 확인됨")
    print(f"   SUPABASE_URL: {supabase_url}")
    print(f"   SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    
    # 각 테스트 실행
    tests = [
        ("Supabase 상세 연결", test_supabase_connection_detailed),
        ("데이터베이스 작업", test_database_operations),
        ("인증 작업", test_auth_operations),
        ("파일 저장소", test_file_storage)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 테스트 실행 중 오류: {str(e)}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "="*50)
    print("📊 테스트 결과 요약")
    print("="*50)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n총 {len(results)}개 테스트 중 {success_count}개 성공")
    
    if success_count == len(results):
        print("\n🎉 모든 테스트가 성공했습니다!")
    else:
        print(f"\n⚠️  {len(results) - success_count}개 테스트가 실패했습니다.")
        print("   환경 변수 설정과 Supabase 프로젝트 설정을 확인하세요.")

if __name__ == "__main__":
    asyncio.run(main())
