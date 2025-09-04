#!/usr/bin/env python3
"""
사용자 조회 기능 테스트 스크립트
"""

import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager

# 환경변수 로드
load_dotenv()

async def test_user_query():
    """사용자 조회 테스트"""
    print("=== 사용자 조회 기능 테스트 ===")
    
    try:
        db_manager = get_db_manager()
        print("✅ 데이터베이스 매니저 생성 성공")
        
        # tester1 사용자 조회
        print("\n--- tester1 사용자 조회 테스트 ---")
        user = await db_manager.get_user_by_username("tester1")
        
        if user:
            print(f"✅ 사용자 조회 성공: {user['username']}")
            print(f"   ID: {user['id']}")
            print(f"   이메일: {user['email']}")
            print(f"   이름: {user['full_name']}")
            print(f"   조직: {user['organization']}")
        else:
            print("❌ 사용자 조회 실패")
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_user_query())
