#!/usr/bin/env python3
"""
로그인 테스트 스크립트
"""
import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager
from auth import get_auth_manager

async def test_login():
    load_dotenv()
    
    print("=== 로그인 테스트 ===")
    
    # 데이터베이스 매니저 초기화
    db_manager = get_db_manager()
    auth_manager = get_auth_manager()
    
    # 베타 테스터 계정 확인
    test_accounts = [
        ("tester1", "beta123!"),
        ("tester2", "beta123!"),
        ("tester3", "beta123!")
    ]
    
    for username, password in test_accounts:
        print(f"\n--- {username} 테스트 ---")
        
        # 1. 데이터베이스에서 사용자 조회
        user = await db_manager.get_user_by_username(username)
        if user:
            print(f"✅ 사용자 {username} 발견")
            print(f"   - ID: {user.get('id')}")
            print(f"   - 사용자명: {user.get('username')}")
            print(f"   - 이메일: {user.get('email')}")
            print(f"   - 비밀번호 해시 존재: {'password_hash' in user}")
        else:
            print(f"❌ 사용자 {username} 없음")
            continue
        
        # 2. 인증 테스트
        try:
            auth_result = await auth_manager.authenticate_user(username, password)
            if auth_result:
                print(f"✅ {username} 인증 성공")
            else:
                print(f"❌ {username} 인증 실패")
        except Exception as e:
            print(f"❌ {username} 인증 오류: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_login())
