#!/usr/bin/env python3
"""
베타 테스터 초기화 스크립트
Supabase 데이터베이스에 베타 테스터 계정들을 생성합니다.
"""

import asyncio
import os
from dotenv import load_dotenv
from auth import create_beta_testers
from database import get_db_manager

async def main():
    """메인 함수"""
    print("🚀 베타 테스터 초기화 시작...")
    
    # 환경변수 로드
    load_dotenv()
    
    try:
        # 데이터베이스 매니저 초기화
        db_manager = get_db_manager()
        
        # 테이블 생성 SQL 출력
        print("\n📋 먼저 Supabase 대시보드에서 다음 SQL을 실행하세요:")
        await db_manager.create_tables()
        
        print("\n⏳ 5초 후 베타 테스터 계정 생성을 시작합니다...")
        await asyncio.sleep(5)
        
        # 베타 테스터 계정 생성
        created_users = await create_beta_testers()
        
        print(f"\n✅ 베타 테스터 초기화 완료!")
        print(f"생성된 계정 수: {len(created_users)}")
        
        print("\n📝 베타 테스터 계정 정보:")
        print("=" * 50)
        print("사용자명: tester1 | 비밀번호: beta123!")
        print("사용자명: tester2 | 비밀번호: beta123!")
        print("사용자명: tester3 | 비밀번호: beta123!")
        print("=" * 50)
        
        print("\n🌐 이제 다음 명령으로 서버를 시작할 수 있습니다:")
        print("python main.py")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print("\n🔧 문제 해결 방법:")
        print("1. .env 파일에 올바른 Supabase 설정이 있는지 확인")
        print("2. Supabase 프로젝트가 활성화되어 있는지 확인")
        print("3. 인터넷 연결 상태 확인")

if __name__ == "__main__":
    asyncio.run(main())
