import os
import asyncio
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
import json

class DatabaseManager:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase URL과 API Key가 설정되지 않았습니다.")
        
        try:
            # Supabase 클라이언트 생성 (옵션 제거)
            self.supabase: Client = create_client(
                self.supabase_url, 
                self.supabase_key
            )
        except Exception as e:
            print(f"Supabase 클라이언트 초기화 오류: {e}")
            # 임시로 None으로 설정하여 오류 방지
            self.supabase = None
    
    async def create_tables(self):
        """테이블 생성 SQL (Supabase 대시보드에서 실행)"""
        sql_commands = [
            # 사용자 테이블
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                organization VARCHAR(100),
                role VARCHAR(20) DEFAULT 'beta_tester',
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # 분석 세션 테이블
            """
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                session_name VARCHAR(200),
                image_count INTEGER NOT NULL,
                analysis_status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                completed_at TIMESTAMP WITH TIME ZONE,
                analysis_result JSONB,
                feedback TEXT,
                feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5)
            );
            """,
            
            # 업로드된 이미지 테이블
            """
            CREATE TABLE IF NOT EXISTS uploaded_images (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_size INTEGER,
                mime_type VARCHAR(100),
                uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # 분석 결과 파일 테이블
            """
            CREATE TABLE IF NOT EXISTS analysis_files (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                file_type VARCHAR(50) NOT NULL, -- 'risk_analysis', 'sgr_checklist', 'recommendations', 'full_report'
                file_path VARCHAR(500) NOT NULL,
                file_size INTEGER,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]
        
        print("다음 SQL 명령어들을 Supabase 대시보드의 SQL Editor에서 실행하세요:")
        for i, sql in enumerate(sql_commands, 1):
            print(f"\n-- 테이블 {i}")
            print(sql)
    
    async def create_user(self, username: str, email: str, password_hash: str, 
                         full_name: str = None, organization: str = None) -> Dict[str, Any]:
        """새 사용자 생성"""
        try:
            result = self.supabase.table('users').insert({
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name,
                'organization': organization
            }).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("사용자 생성 실패")
        except Exception as e:
            raise Exception(f"사용자 생성 중 오류: {str(e)}")
    
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """사용자명으로 사용자 조회"""
        try:
            result = self.supabase.table('users').select('*').eq('username', username).execute()
            print(f"사용자 조회 결과: {result}")
            print(f"결과 데이터: {result.data}")
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                print(f"사용자 '{username}'을 찾을 수 없습니다.")
                return None
        except Exception as e:
            print(f"사용자 조회 중 오류: {str(e)}")
            return None
    
    async def create_analysis_session(self, user_id: str, session_name: str, 
                                    image_count: int) -> Dict[str, Any]:
        """새 분석 세션 생성"""
        try:
            result = self.supabase.table('analysis_sessions').insert({
                'user_id': user_id,
                'session_name': session_name,
                'image_count': image_count
            }).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("분석 세션 생성 실패")
        except Exception as e:
            raise Exception(f"분석 세션 생성 중 오류: {str(e)}")
    
    async def save_uploaded_image(self, session_id: str, user_id: str, 
                                filename: str, file_path: str, 
                                file_size: int, mime_type: str) -> Dict[str, Any]:
        """업로드된 이미지 정보 저장"""
        try:
            result = self.supabase.table('uploaded_images').insert({
                'session_id': session_id,
                'user_id': user_id,
                'filename': filename,
                'file_path': file_path,
                'file_size': file_size,
                'mime_type': mime_type
            }).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("이미지 정보 저장 실패")
        except Exception as e:
            raise Exception(f"이미지 정보 저장 중 오류: {str(e)}")
    
    async def save_analysis_result(self, session_id: str, user_id: str, 
                                 analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """분석 결과 저장"""
        try:
            # 서울 시간대 (UTC+9)
            seoul_tz = timezone(timedelta(hours=9))
            seoul_time = datetime.now(seoul_tz)
            
            result = self.supabase.table('analysis_sessions').update({
                'analysis_result': analysis_result,
                'analysis_status': 'completed',
                'completed_at': seoul_time.isoformat()
            }).eq('id', session_id).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("분석 결과 저장 실패")
        except Exception as e:
            raise Exception(f"분석 결과 저장 중 오류: {str(e)}")
    
    async def save_feedback(self, session_id: str, feedback: str, rating: int) -> Dict[str, Any]:
        """피드백 저장"""
        try:
            result = self.supabase.table('analysis_sessions').update({
                'feedback': feedback,
                'feedback_rating': rating
            }).eq('id', session_id).execute()
            
            if result.data:
                return result.data[0]
            else:
                raise Exception("피드백 저장 실패")
        except Exception as e:
            raise Exception(f"피드백 저장 중 오류: {str(e)}")
    
    async def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """사용자의 분석 세션 목록 조회"""
        try:
            result = self.supabase.table('analysis_sessions').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"세션 목록 조회 중 오류: {str(e)}")
            return []
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """모든 사용자 조회"""
        try:
            result = self.supabase.table('users').select('*').order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"사용자 목록 조회 중 오류: {str(e)}")
            return []
    
    async def get_all_sessions(self) -> List[Dict[str, Any]]:
        """모든 분석 세션 조회"""
        try:
            result = self.supabase.table('analysis_sessions').select('*').order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"세션 목록 조회 중 오류: {str(e)}")
            return []
    
    async def get_all_images(self) -> List[Dict[str, Any]]:
        """모든 업로드된 이미지 조회"""
        try:
            result = self.supabase.table('uploaded_images').select('*').order('uploaded_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"이미지 목록 조회 중 오류: {str(e)}")
            return []

# 전역 데이터베이스 매니저 인스턴스
db_manager = None

def get_db_manager() -> DatabaseManager:
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager
