#!/usr/bin/env python3
"""
Supabase 데이터 확인 스크립트
베타 테스트 결과가 제대로 저장되고 있는지 확인
"""

import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager

# 환경변수 로드
load_dotenv()

async def check_supabase_data():
    """Supabase에 저장된 데이터 확인"""
    print("🔍 Supabase 데이터 확인 시작")
    print("=" * 50)
    
    try:
        db_manager = get_db_manager()
        
        # 1. 사용자 계정 확인
        print("\n👥 사용자 계정 정보:")
        print("-" * 30)
        users = await db_manager.get_all_users()
        if users:
            for user in users:
                print(f"  • {user['username']} ({user['full_name']}) - {user['organization']}")
                print(f"    역할: {user['role']}, 활성화: {user['is_active']}")
                print(f"    생성일: {user['created_at']}")
                print()
        else:
            print("  ❌ 사용자 데이터가 없습니다.")
        
        # 2. 분석 세션 확인
        print("\n📊 분석 세션 정보:")
        print("-" * 30)
        sessions = await db_manager.get_all_sessions()
        if sessions:
            for session in sessions:
                print(f"  • 세션: {session['session_name']}")
                print(f"    사용자 ID: {session['user_id']}")
                print(f"    이미지 수: {session['image_count']}")
                print(f"    상태: {session['analysis_status']}")
                print(f"    생성일: {session['created_at']}")
                if session.get('completed_at'):
                    print(f"    완료일: {session['completed_at']}")
                if session.get('feedback'):
                    print(f"    피드백: {session['feedback'][:50]}...")
                if session.get('feedback_rating'):
                    print(f"    평점: {session['feedback_rating']}/5")
                print()
        else:
            print("  ❌ 분석 세션 데이터가 없습니다.")
        
        # 3. 업로드된 이미지 확인
        print("\n🖼️ 업로드된 이미지 정보:")
        print("-" * 30)
        images = await db_manager.get_all_images()
        if images:
            for image in images:
                print(f"  • {image['filename']}")
                print(f"    세션 ID: {image['session_id']}")
                print(f"    파일 크기: {image['file_size']} bytes")
                print(f"    업로드일: {image['uploaded_at']}")
                print()
        else:
            print("  ❌ 이미지 데이터가 없습니다.")
        
        # 4. 통계 정보
        print("\n📈 데이터 통계:")
        print("-" * 30)
        if users:
            print(f"  • 총 사용자 수: {len(users)}명")
        if sessions:
            print(f"  • 총 분석 세션 수: {len(sessions)}개")
            completed_sessions = [s for s in sessions if s['analysis_status'] == 'completed']
            print(f"  • 완료된 세션 수: {len(completed_sessions)}개")
            pending_sessions = [s for s in sessions if s['analysis_status'] == 'pending']
            print(f"  • 진행 중인 세션 수: {len(pending_sessions)}개")
        if images:
            print(f"  • 총 업로드된 이미지 수: {len(images)}장")
        
        print("\n✅ 데이터 확인 완료!")
        
    except Exception as e:
        print(f"❌ 데이터 확인 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_supabase_data())
