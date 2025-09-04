#!/usr/bin/env python3
"""
간단한 베타 테스터 생성 스크립트 (requests 사용)
"""
import os
import requests
import hashlib
import secrets
from dotenv import load_dotenv

def hash_password(password: str) -> str:
    """간단한 비밀번호 해싱 (bcrypt 대신)"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

def create_beta_testers():
    print("=== 베타 테스터 생성 (간단한 방법) ===")
    
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase 설정이 없습니다")
        return
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    # 베타 테스터 계정 정보
    beta_testers = [
        {
            'username': 'tester1',
            'email': 'tester1@beta.com',
            'password': 'beta123!',
            'full_name': '베타 테스터 1',
            'organization': 'Beta Test Group'
        },
        {
            'username': 'tester2', 
            'email': 'tester2@beta.com',
            'password': 'beta123!',
            'full_name': '베타 테스터 2',
            'organization': 'Beta Test Group'
        },
        {
            'username': 'tester3',
            'email': 'tester3@beta.com', 
            'password': 'beta123!',
            'full_name': '베타 테스터 3',
            'organization': 'Beta Test Group'
        }
    ]
    
    for tester in beta_testers:
        print(f"\n--- {tester['username']} 생성 중 ---")
        
        # 비밀번호 해싱
        password_hash = hash_password(tester['password'])
        
        # 사용자 데이터
        user_data = {
            'username': tester['username'],
            'email': tester['email'],
            'password_hash': password_hash,
            'full_name': tester['full_name'],
            'organization': tester['organization'],
            'role': 'beta_tester',
            'is_active': True
        }
        
        try:
            # 사용자 생성
            response = requests.post(
                f"{supabase_url}/rest/v1/users",
                headers=headers,
                json=user_data
            )
            
            if response.status_code == 201:
                print(f"✅ {tester['username']} 생성 성공")
            elif response.status_code == 409:
                print(f"⚠️ {tester['username']} 이미 존재함")
            else:
                print(f"❌ {tester['username']} 생성 실패: {response.status_code}")
                print(f"응답: {response.text}")
                
        except Exception as e:
            print(f"❌ {tester['username']} 생성 오류: {str(e)}")
    
    print("\n=== 베타 테스터 계정 정보 ===")
    print("사용자명: tester1, tester2, tester3")
    print("비밀번호: beta123!")
    print("\n이제 웹 애플리케이션에서 로그인을 시도해보세요!")

if __name__ == "__main__":
    create_beta_testers()

