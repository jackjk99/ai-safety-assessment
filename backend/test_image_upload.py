#!/usr/bin/env python3
"""
이미지 업로드 기능 테스트 스크립트
"""

import asyncio
import os
from dotenv import load_dotenv
from database import get_db_manager
from file_storage import get_file_storage_manager

# 환경변수 로드
load_dotenv()

async def test_image_upload():
    """이미지 업로드 테스트"""
    print("=== 이미지 업로드 기능 테스트 ===")
    
    try:
        # 데이터베이스 매니저 테스트
        print("\n1. 데이터베이스 연결 테스트")
        db_manager = get_db_manager()
        print("✅ 데이터베이스 매니저 생성 성공")
        
        # 파일 스토리지 매니저 테스트
        print("\n2. 파일 스토리지 매니저 테스트")
        file_storage = get_file_storage_manager()
        print("✅ 파일 스토리지 매니저 생성 성공")
        
        # 업로드 디렉토리 확인
        print("\n3. 업로드 디렉토리 확인")
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"✅ 업로드 디렉토리 생성: {upload_dir}")
        else:
            print(f"✅ 업로드 디렉토리 존재: {upload_dir}")
        
        # 디렉토리 권한 확인
        if os.access(upload_dir, os.W_OK):
            print("✅ 업로드 디렉토리 쓰기 권한 확인")
        else:
            print("❌ 업로드 디렉토리 쓰기 권한 없음")
            
        print("\n=== 테스트 완료 ===")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_image_upload())
