#!/usr/bin/env python3
"""
Supabase 연결 테스트 스크립트
"""
import os
import requests
from dotenv import load_dotenv

def test_supabase_connection():
    print("=== Supabase 연결 테스트 ===")
    
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase URL 또는 Key가 설정되지 않음")
        return
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:20]}...")
    
    # 1. 기본 연결 테스트
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        # 간단한 API 호출 테스트
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers)
        print(f"기본 연결 테스트: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Supabase 연결 성공")
        else:
            print(f"❌ Supabase 연결 실패: {response.status_code}")
            print(f"응답: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 연결 오류: {str(e)}")
    
    # 2. users 테이블 확인
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{supabase_url}/rest/v1/users?select=*&limit=1", headers=headers)
        print(f"users 테이블 테스트: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ users 테이블 접근 성공")
            data = response.json()
            print(f"사용자 수: {len(data)}")
        else:
            print(f"❌ users 테이블 접근 실패: {response.status_code}")
            print(f"응답: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ users 테이블 오류: {str(e)}")

if __name__ == "__main__":
    test_supabase_connection()

