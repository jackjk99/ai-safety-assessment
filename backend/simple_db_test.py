#!/usr/bin/env python3
"""
간단한 데이터베이스 연결 테스트
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_supabase_connection():
    """Supabase 연결 테스트"""
    
    # 환경변수 로드
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    print("🔍 Supabase 연결 테스트")
    print("=" * 40)
    
    if not supabase_url or not supabase_key:
        print("❌ 환경변수가 설정되지 않았습니다.")
        print("SUPABASE_URL:", supabase_url)
        print("SUPABASE_ANON_KEY:", supabase_key[:20] + "..." if supabase_key else "None")
        return False
    
    print("✅ 환경변수 확인됨")
    print(f"URL: {supabase_url}")
    print(f"Key: {supabase_key[:20]}...")
    
    # 간단한 API 테스트
    try:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        
        # users 테이블 조회 테스트
        response = requests.get(
            f"{supabase_url}/rest/v1/users?select=*&limit=1",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Supabase 연결 성공!")
            print("✅ users 테이블 접근 가능")
            return True
        else:
            print(f"❌ API 요청 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
        return False

def create_test_users():
    """테스트 사용자 생성"""
    
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ 환경변수가 설정되지 않았습니다.")
        return
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    # 테스트 사용자 데이터
    test_users = [
        {
            "username": "tester1",
            "email": "tester1@example.com",
            "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K.5.5O",  # beta123!
            "full_name": "테스터 1",
            "organization": "건설회사 A"
        },
        {
            "username": "tester2",
            "email": "tester2@example.com", 
            "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K.5.5O",  # beta123!
            "full_name": "테스터 2",
            "organization": "안전관리업체 B"
        },
        {
            "username": "tester3",
            "email": "tester3@example.com",
            "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K.5.5O",  # beta123!
            "full_name": "테스터 3", 
            "organization": "건설회사 C"
        }
    ]
    
    print("\n👥 테스트 사용자 생성 시도")
    print("-" * 30)
    
    for user in test_users:
        try:
            response = requests.post(
                f"{supabase_url}/rest/v1/users",
                headers=headers,
                json=user
            )
            
            if response.status_code == 201:
                print(f"✅ {user['username']} 생성 성공")
            elif response.status_code == 409:
                print(f"⚠️ {user['username']} 이미 존재함")
            else:
                print(f"❌ {user['username']} 생성 실패: {response.status_code}")
                print(f"응답: {response.text}")
                
        except Exception as e:
            print(f"❌ {user['username']} 생성 오류: {e}")

def main():
    """메인 함수"""
    print("🚀 Supabase 데이터베이스 테스트")
    print("=" * 50)
    
    # 연결 테스트
    if test_supabase_connection():
        # 사용자 생성 시도
        create_test_users()
        
        print("\n" + "=" * 50)
        print("✅ 테스트 완료!")
        print("\n💡 베타 테스트 계정:")
        print("   - tester1 / beta123!")
        print("   - tester2 / beta123!")
        print("   - tester3 / beta123!")
    else:
        print("\n❌ Supabase 연결에 실패했습니다.")
        print("환경변수 설정을 확인해주세요.")

if __name__ == "__main__":
    main()
