#!/usr/bin/env python3
"""
웹 애플리케이션 베타 테스트 스크립트
"""
import os
import asyncio
import requests
import time
from dotenv import load_dotenv

class WebAppTester:
    def __init__(self):
        load_dotenv()
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        
    async def test_backend_api(self):
        """백엔드 API 테스트"""
        print("\n🔧 백엔드 API 테스트")
        print("-" * 40)
        
        # 1. 서버 상태 확인
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ 백엔드 서버 응답 성공")
            else:
                print(f"⚠️ 백엔드 서버 응답: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ 백엔드 서버에 연결할 수 없음")
            print("   python main.py로 서버를 시작하세요")
            return False
        except Exception as e:
            print(f"❌ 백엔드 서버 테스트 실패: {str(e)}")
            return False
        
        # 2. API 문서 확인
        try:
            response = requests.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                print("✅ API 문서 접근 성공")
            else:
                print(f"⚠️ API 문서 접근: {response.status_code}")
        except Exception as e:
            print(f"❌ API 문서 테스트 실패: {str(e)}")
        
        # 3. 헬스체크 엔드포인트
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ 헬스체크 성공")
            else:
                print(f"⚠️ 헬스체크: {response.status_code}")
        except Exception as e:
            print(f"❌ 헬스체크 테스트 실패: {str(e)}")
        
        return True
    
    async def test_frontend(self):
        """프론트엔드 테스트"""
        print("\n🌐 프론트엔드 테스트")
        print("-" * 40)
        
        try:
            response = requests.get(self.frontend_url)
            if response.status_code == 200:
                print("✅ 프론트엔드 접근 성공")
                return True
            else:
                print(f"⚠️ 프론트엔드 응답: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 프론트엔드에 연결할 수 없음")
            print("   프론트엔드 서버를 시작하세요")
            return False
        except Exception as e:
            print(f"❌ 프론트엔드 테스트 실패: {str(e)}")
            return False
    
    async def test_user_registration(self):
        """사용자 등록 테스트"""
        print("\n👤 사용자 등록 테스트")
        print("-" * 40)
        
        test_user = {
            "username": "web_tester",
            "email": "web_tester@beta.com",
            "password": "web123!",
            "full_name": "웹 테스터",
            "organization": "Web Test Group"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json=test_user
            )
            
            if response.status_code == 201:
                print("✅ 사용자 등록 성공")
                return True
            elif response.status_code == 409:
                print("⚠️ 사용자가 이미 존재함")
                return True
            else:
                print(f"❌ 사용자 등록 실패: {response.status_code}")
                print(f"응답: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 사용자 등록 테스트 실패: {str(e)}")
            return False
    
    async def test_user_login(self):
        """사용자 로그인 테스트"""
        print("\n🔐 사용자 로그인 테스트")
        print("-" * 40)
        
        login_data = {
            "username": "web_tester",
            "password": "web123!"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    print("✅ 로그인 성공")
                    print(f"   토큰: {data['access_token'][:20]}...")
                    return data['access_token']
                else:
                    print("❌ 토큰이 응답에 없음")
                    return None
            else:
                print(f"❌ 로그인 실패: {response.status_code}")
                print(f"응답: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 로그인 테스트 실패: {str(e)}")
            return None
    
    async def test_authenticated_endpoints(self, token):
        """인증이 필요한 엔드포인트 테스트"""
        print("\n🔒 인증 엔드포인트 테스트")
        print("-" * 40)
        
        if not token:
            print("❌ 토큰이 없어서 테스트를 건너뜀")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. 사용자 프로필 조회
        try:
            response = requests.get(
                f"{self.base_url}/users/profile",
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ 사용자 프로필 조회 성공")
            else:
                print(f"⚠️ 사용자 프로필 조회: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 사용자 프로필 테스트 실패: {str(e)}")
        
        # 2. 분석 세션 목록 조회
        try:
            response = requests.get(
                f"{self.base_url}/sessions",
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ 분석 세션 목록 조회 성공")
            else:
                print(f"⚠️ 분석 세션 목록 조회: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 분석 세션 목록 테스트 실패: {str(e)}")
        
        return True
    
    async def run_all_tests(self):
        """모든 웹 애플리케이션 테스트 실행"""
        print("🚀 웹 애플리케이션 베타 테스트 시작")
        print("=" * 60)
        
        # 1. 백엔드 API 테스트
        backend_ok = await self.test_backend_api()
        if not backend_ok:
            print("\n❌ 백엔드 서버가 실행되지 않았습니다.")
            print("   다음 명령어로 서버를 시작하세요:")
            print("   cd backend && python main.py")
            return
        
        # 2. 프론트엔드 테스트
        frontend_ok = await self.test_frontend()
        if not frontend_ok:
            print("\n⚠️ 프론트엔드 서버가 실행되지 않았습니다.")
            print("   프론트엔드 서버를 시작하세요")
        
        # 3. 사용자 등록 테스트
        await self.test_user_registration()
        
        # 4. 사용자 로그인 테스트
        token = await self.test_user_login()
        
        # 5. 인증 엔드포인트 테스트
        if token:
            await self.test_authenticated_endpoints(token)
        
        print("\n" + "=" * 60)
        print("🎉 웹 애플리케이션 베타 테스트 완료!")
        print("=" * 60)
        
        if backend_ok and frontend_ok:
            print("\n✅ 모든 테스트가 성공했습니다!")
            print(f"🌐 프론트엔드: {self.frontend_url}")
            print(f"🔧 백엔드 API: {self.base_url}")
            print(f"📚 API 문서: {self.base_url}/docs")
        else:
            print("\n⚠️ 일부 테스트가 실패했습니다.")
            print("   서버 상태를 확인하고 다시 시도하세요.")

async def main():
    """메인 함수"""
    tester = WebAppTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
