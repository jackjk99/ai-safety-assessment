#!/usr/bin/env python3
"""
환경 변수 확인 스크립트
"""
import os
from dotenv import load_dotenv

def check_env():
    print("=== 환경 변수 확인 ===")
    
    # .env 파일 로드
    load_dotenv()
    
    # 환경 변수 확인
    env_vars = [
        'OPENAI_API_KEY',
        'SUPABASE_URL', 
        'SUPABASE_ANON_KEY',
        'SECRET_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'KEY' in var or 'SECRET' in var:
                # 보안상 일부만 표시
                display_value = value[:10] + "..." if len(value) > 10 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 설정되지 않음")
    
    print("\n=== .env 파일 경로 확인 ===")
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    print(f".env 파일 경로: {env_file_path}")
    print(f".env 파일 존재: {os.path.exists(env_file_path)}")
    
    if os.path.exists(env_file_path):
        print("\n=== .env 파일 내용 (일부) ===")
        try:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:5]):  # 처음 5줄만 표시
                    if 'KEY' in line or 'SECRET' in line:
                        # 보안상 키 값은 마스킹
                        parts = line.split('=')
                        if len(parts) == 2:
                            key, value = parts
                            masked_value = value[:10] + "..." if len(value.strip()) > 10 else value
                            print(f"{i+1}: {key}={masked_value}")
                        else:
                            print(f"{i+1}: {line.strip()}")
                    else:
                        print(f"{i+1}: {line.strip()}")
        except Exception as e:
            print(f"파일 읽기 오류: {e}")

if __name__ == "__main__":
    check_env()

