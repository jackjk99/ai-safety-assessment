#!/usr/bin/env python3
"""
베타 테스트 실행 스크립트
"""
import os
import asyncio
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

class BetaTestRunner:
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
    async def run_all_tests(self):
        """모든 베타 테스트 실행"""
        print("🚀 베타 테스트 시작")
        print("=" * 60)
        
        # 1. 기본 연결 테스트
        await self.test_basic_connection()
        
        # 2. 베타 테스터 계정 생성
        await self.create_beta_testers()
        
        # 3. 로그인 테스트
        await self.test_login()
        
        # 4. 이미지 업로드 테스트
        await self.test_image_upload()
        
        # 5. 분석 세션 테스트
        await self.test_analysis_session()
        
        print("\n" + "=" * 60)
        print("🎉 베타 테스트 완료!")
        print("=" * 60)
    
    async def test_basic_connection(self):
        """기본 연결 테스트"""
        print("\n📡 1. 기본 연결 테스트")
        print("-" * 40)
        
        try:
            # Supabase 연결 테스트
            response = self.supabase.table('users').select('*').limit(1).execute()
            print("✅ Supabase 연결 성공")
            
            # 테이블 접근 테스트
            tables = ['users', 'analysis_sessions', 'uploaded_images', 'analysis_files']
            for table in tables:
                try:
                    response = self.supabase.table(table).select('*').limit(1).execute()
                    print(f"✅ {table} 테이블 접근 성공")
                except Exception as e:
                    print(f"❌ {table} 테이블 접근 실패: {str(e)}")
                    
        except Exception as e:
            print(f"❌ 기본 연결 테스트 실패: {str(e)}")
    
    async def create_beta_testers(self):
        """베타 테스터 계정 생성"""
        print("\n👥 2. 베타 테스터 계정 생성")
        print("-" * 40)
        
        beta_testers = [
            {
                'username': 'tester1',
                'email': 'tester1@beta.com',
                'password': 'beta123!',
                'full_name': '베타 테스터 1',
                'organization': 'Beta Test Group'
            },
            {
                'username': 'tester2', 
                'email': 'tester2@beta.com',
                'password': 'beta123!',
                'full_name': '베타 테스터 2',
                'organization': 'Beta Test Group'
            },
            {
                'username': 'tester3',
                'email': 'tester3@beta.com', 
                'password': 'beta123!',
                'full_name': '베타 테스터 3',
                'organization': 'Beta Test Group'
            }
        ]
        
        for tester in beta_testers:
            print(f"\n--- {tester['username']} 생성 중 ---")
            
            try:
                # 사용자 데이터
                user_data = {
                    'username': tester['username'],
                    'email': tester['email'],
                    'password_hash': f"hashed_{tester['password']}",  # 실제로는 bcrypt 사용
                    'full_name': tester['full_name'],
                    'organization': tester['organization'],
                    'role': 'beta_tester',
                    'is_active': True
                }
                
                # 사용자 생성
                response = self.supabase.table('users').insert(user_data).execute()
                
                if response.data:
                    print(f"✅ {tester['username']} 생성 성공")
                else:
                    print(f"⚠️ {tester['username']} 이미 존재하거나 생성 실패")
                    
            except Exception as e:
                print(f"❌ {tester['username']} 생성 오류: {str(e)}")
    
    async def test_login(self):
        """로그인 테스트"""
        print("\n🔐 3. 로그인 테스트")
        print("-" * 40)
        
        try:
            # 사용자 조회 테스트
            response = self.supabase.table('users').select('*').eq('username', 'tester1').execute()
            
            if response.data:
                user = response.data[0]
                print(f"✅ 사용자 조회 성공: {user['username']}")
                print(f"   역할: {user['role']}")
                print(f"   활성화: {user['is_active']}")
            else:
                print("❌ 사용자 조회 실패")
                
        except Exception as e:
            print(f"❌ 로그인 테스트 실패: {str(e)}")
    
    async def test_image_upload(self):
        """이미지 업로드 테스트"""
        print("\n📸 4. 이미지 업로드 테스트")
        print("-" * 40)
        
        try:
            # 테스트 이미지 정보
            test_image = {
                'filename': 'test_image.jpg',
                'file_path': '/test/path/test_image.jpg',
                'file_size': 1024,
                'mime_type': 'image/jpeg'
            }
            
            # 사용자 ID 가져오기
            user_response = self.supabase.table('users').select('id').eq('username', 'tester1').execute()
            if not user_response.data:
                print("❌ 테스트 사용자를 찾을 수 없음")
                return
                
            user_id = user_response.data[0]['id']
            
            # 분석 세션 생성
            session_data = {
                'user_id': user_id,
                'session_name': '테스트 세션',
                'image_count': 1
            }
            
            session_response = self.supabase.table('analysis_sessions').insert(session_data).execute()
            
            if session_response.data:
                session_id = session_response.data[0]['id']
                print(f"✅ 분석 세션 생성 성공: {session_id}")
                
                # 이미지 정보 저장
                image_data = {
                    'session_id': session_id,
                    'user_id': user_id,
                    **test_image
                }
                
                image_response = self.supabase.table('uploaded_images').insert(image_data).execute()
                
                if image_response.data:
                    print("✅ 이미지 정보 저장 성공")
                else:
                    print("❌ 이미지 정보 저장 실패")
            else:
                print("❌ 분석 세션 생성 실패")
                
        except Exception as e:
            print(f"❌ 이미지 업로드 테스트 실패: {str(e)}")
    
    async def test_analysis_session(self):
        """분석 세션 테스트"""
        print("\n🔍 5. 분석 세션 테스트")
        print("-" * 40)
        
        try:
            # 사용자 ID 가져오기
            user_response = self.supabase.table('users').select('id').eq('username', 'tester1').execute()
            if not user_response.data:
                print("❌ 테스트 사용자를 찾을 수 없음")
                return
                
            user_id = user_response.data[0]['id']
            
            # 사용자의 분석 세션 조회
            sessions_response = self.supabase.table('analysis_sessions').select('*').eq('user_id', user_id).execute()
            
            if sessions_response.data:
                print(f"✅ 분석 세션 조회 성공: {len(sessions_response.data)}개 세션")
                
                for session in sessions_response.data:
                    print(f"   - 세션: {session['session_name']}")
                    print(f"     상태: {session['analysis_status']}")
                    print(f"     이미지 수: {session['image_count']}")
            else:
                print("❌ 분석 세션 조회 실패")
                
        except Exception as e:
            print(f"❌ 분석 세션 테스트 실패: {str(e)}")

async def main():
    """메인 함수"""
    runner = BetaTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
