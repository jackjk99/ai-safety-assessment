#!/usr/bin/env python3
"""
업로드된 이미지 확인 스크립트
Supabase의 uploaded_images 테이블에서 이미지 정보 조회
"""

import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager
from datetime import datetime, timezone, timedelta

# 환경변수 로드
load_dotenv()

async def check_uploaded_images():
    """업로드된 이미지 정보 확인"""
    print("🖼️ 업로드된 이미지 확인 시작")
    print("=" * 50)
    
    try:
        db_manager = get_db_manager()
        
        # 1. 모든 이미지 조회
        print("\n📸 업로드된 이미지 목록:")
        print("-" * 40)
        images = await db_manager.get_all_images()
        
        if images:
            for i, image in enumerate(images, 1):
                print(f"\n{i}. {image['filename']}")
                print(f"   📁 파일 경로: {image['file_path']}")
                print(f"   📏 파일 크기: {image['file_size']:,} bytes")
                print(f"   🏷️ MIME 타입: {image['mime_type']}")
                print(f"   👤 사용자 ID: {image['user_id']}")
                print(f"   🔗 세션 ID: {image['session_id']}")
                # UTC 시간을 서울 시간으로 변환
                try:
                    utc_time = datetime.fromisoformat(image['uploaded_at'].replace('Z', '+00:00'))
                    seoul_tz = timezone(timedelta(hours=9))
                    seoul_time = utc_time.astimezone(seoul_tz)
                    print(f"   📅 업로드 시간 (서울): {seoul_time.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"   📅 업로드 시간: {image['uploaded_at']}")
                
                # 파일 존재 여부 확인
                if os.path.exists(image['file_path']):
                    print(f"   ✅ 파일 존재: 예")
                else:
                    print(f"   ❌ 파일 존재: 아니오 (삭제됨)")
        else:
            print("  ❌ 업로드된 이미지가 없습니다.")
        
        # 2. 통계 정보
        print(f"\n📊 이미지 통계:")
        print("-" * 40)
        if images:
            total_size = sum(img['file_size'] for img in images)
            unique_users = len(set(img['user_id'] for img in images))
            unique_sessions = len(set(img['session_id'] for img in images))
            
            print(f"  • 총 이미지 수: {len(images)}장")
            print(f"  • 총 파일 크기: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
            print(f"  • 사용자 수: {unique_users}명")
            print(f"  • 세션 수: {unique_sessions}개")
            
            # MIME 타입별 통계
            mime_types = {}
            for img in images:
                mime_type = img['mime_type']
                mime_types[mime_type] = mime_types.get(mime_type, 0) + 1
            
            print(f"\n  📋 MIME 타입별 분포:")
            for mime_type, count in mime_types.items():
                print(f"    • {mime_type}: {count}장")
        
        # 3. 최근 업로드된 이미지 (최대 5개)
        print(f"\n🕒 최근 업로드된 이미지 (최대 5개):")
        print("-" * 40)
        if images:
            recent_images = sorted(images, key=lambda x: x['uploaded_at'], reverse=True)[:5]
            for i, image in enumerate(recent_images, 1):
                print(f"  {i}. {image['filename']} - {image['uploaded_at']}")
        
        print("\n✅ 이미지 확인 완료!")
        
    except Exception as e:
        print(f"❌ 이미지 확인 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_uploaded_images())
