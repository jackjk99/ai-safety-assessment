#!/usr/bin/env python3
"""
간단한 베타 테스트용 스크립트 (Supabase 없이)
"""

import os
import hashlib
from datetime import datetime

def create_simple_beta_testers():
    """간단한 베타 테스터 계정 정보 생성"""
    
    print("🚀 베타 테스터 계정 정보 생성")
    print("=" * 50)
    
    # 베타 테스터 정보
    beta_testers = [
        {
            "username": "tester1",
            "email": "tester1@example.com",
            "password": "beta123!",
            "full_name": "테스터 1",
            "organization": "건설회사 A"
        },
        {
            "username": "tester2", 
            "email": "tester2@example.com",
            "password": "beta123!",
            "full_name": "테스터 2",
            "organization": "안전관리업체 B"
        },
        {
            "username": "tester3",
            "email": "tester3@example.com", 
            "password": "beta123!",
            "full_name": "테스터 3",
            "organization": "건설회사 C"
        }
    ]
    
    print("📝 베타 테스터 계정 정보:")
    print("-" * 30)
    
    for i, tester in enumerate(beta_testers, 1):
        print(f"{i}. 사용자명: {tester['username']}")
        print(f"   비밀번호: {tester['password']}")
        print(f"   이름: {tester['full_name']}")
        print(f"   조직: {tester['organization']}")
        print(f"   이메일: {tester['email']}")
        print()
    
    print("=" * 50)
    print("✅ 베타 테스터 계정 정보가 준비되었습니다!")
    print()
    print("📋 다음 단계:")
    print("1. Supabase 프로젝트를 생성하세요")
    print("2. 위의 SQL을 Supabase 대시보드에서 실행하세요")
    print("3. .env 파일에 Supabase 설정을 추가하세요")
    print("4. python main.py로 서버를 시작하세요")
    print()
    print("🌐 접속 주소:")
    print("- 프론트엔드: http://localhost:3000")
    print("- 백엔드 API: http://localhost:8000")
    print("- API 문서: http://localhost:8000/docs")

if __name__ == "__main__":
    create_simple_beta_testers()
