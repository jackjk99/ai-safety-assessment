#!/usr/bin/env python3
"""
베타 테스터 계정 재생성 스크립트
기존 계정을 삭제하고 올바른 비밀번호 해시로 재생성
"""

import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager
from auth import get_auth_manager

# 환경변수 로드
load_dotenv()

async def recreate_beta_testers():
    """베타 테스터 계정 재생성"""
    print("=== 베타 테스터 계정 재생성 ===")
    
    db_manager = get_db_manager()
    auth_manager = get_auth_manager()
    
    # 기존 베타 테스터 계정 삭제
    print("\n1. 기존 베타 테스터 계정 삭제 중...")
    try:
        # users 테이블에서 베타 테스터 계정 삭제
        result = db_manager.supabase.table('users').delete().in_('username', ['tester1', 'tester2', 'tester3']).execute()
        print(f"삭제된 계정 수: {len(result.data) if result.data else 0}")
    except Exception as e:
        print(f"계정 삭제 중 오류: {e}")
    
    # 새로운 베타 테스터 계정 생성
    print("\n2. 새로운 베타 테스터 계정 생성 중...")
    
    beta_testers = [
        {
            "username": "tester1",
            "email": "tester1@beta.com",
            "password": "beta123!",
            "full_name": "베타 테스터 1",
            "organization": "Beta Test Group"
        },
        {
            "username": "tester2",
            "email": "tester2@beta.com",
            "password": "beta123!",
            "full_name": "베타 테스터 2",
            "organization": "Beta Test Group"
        },
        {
            "username": "tester3",
            "email": "tester3@beta.com",
            "password": "beta123!",
            "full_name": "베타 테스터 3",
            "organization": "Beta Test Group"
        }
    ]
    
    created_users = []
    for tester in beta_testers:
        try:
            print(f"\n--- {tester['username']} 생성 중 ---")
            user = await auth_manager.register_user(**tester)
            created_users.append(user)
            print(f"✅ {tester['username']} 생성 성공")
        except Exception as e:
            print(f"❌ {tester['username']} 생성 실패: {e}")
    
    print(f"\n=== 생성 완료 ===")
    print(f"성공적으로 생성된 계정: {len(created_users)}개")
    
    if created_users:
        print("\n=== 베타 테스터 계정 정보 ===")
        print("사용자명: tester1, tester2, tester3")
        print("비밀번호: beta123!")
        print("\n이제 웹 애플리케이션에서 로그인을 시도해보세요!")
    
    return created_users

if __name__ == "__main__":
    asyncio.run(recreate_beta_testers())
