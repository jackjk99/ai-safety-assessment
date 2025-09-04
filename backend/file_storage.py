import os
import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import aiofiles
from fastapi import UploadFile, HTTPException
from database import get_db_manager

class FileStorageManager:
    def __init__(self):
        self.base_storage_path = Path("storage")
        self.images_path = self.base_storage_path / "images"
        self.results_path = self.base_storage_path / "results"
        self.reports_path = self.base_storage_path / "reports"
        
        # 디렉토리 생성
        self._create_directories()
    
    def _create_directories(self):
        """저장 디렉토리 생성"""
        for path in [self.images_path, self.results_path, self.reports_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _get_user_directory(self, user_id: str, base_path: Path) -> Path:
        """사용자별 디렉토리 경로 생성"""
        user_dir = base_path / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def _get_session_directory(self, user_id: str, session_id: str, base_path: Path) -> Path:
        """세션별 디렉토리 경로 생성 - 날짜폴더 > 사용자ID_시간 형태"""
        # 서울 시간대 (UTC+9)
        seoul_tz = timezone(timedelta(hours=9))
        seoul_time = datetime.now(seoul_tz)
        
        # 날짜 폴더 (YYYY-MM-DD)
        date_folder = seoul_time.strftime("%Y-%m-%d")
        
        # 사용자ID_시간 폴더 (예: tester1_2025-09-03_14-30-25)
        time_str = seoul_time.strftime("%H-%M-%S")
        user_time_folder = f"{user_id}_{time_str}"
        
        # 전체 경로: storage/images/2025-09-03/tester1_14-30-25/
        session_dir = base_path / date_folder / user_time_folder
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir
    
    async def save_uploaded_images(self, session_id: str, user_id: str, 
                                 files: List[UploadFile]) -> List[Dict[str, Any]]:
        """업로드된 이미지 파일들 저장"""
        db_manager = get_db_manager()
        session_dir = self._get_session_directory(user_id, session_id, self.images_path)
        saved_images = []
        
        for file in files:
            if not file.content_type.startswith('image/'):
                continue
            
            # 고유한 파일명 생성
            file_extension = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = session_dir / unique_filename
            
            # 파일 저장
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # 데이터베이스에 정보 저장
            image_info = await db_manager.save_uploaded_image(
                session_id=session_id,
                user_id=user_id,
                filename=file.filename,
                file_path=str(file_path),
                file_size=len(content),
                mime_type=file.content_type
            )
            
            saved_images.append({
                "id": image_info["id"],
                "original_filename": file.filename,
                "stored_filename": unique_filename,
                "file_path": str(file_path),
                "file_size": len(content),
                "mime_type": file.content_type
            })
        
        return saved_images
    
    async def save_analysis_results(self, session_id: str, user_id: str, 
                                  analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """분석 결과 파일들 저장"""
        db_manager = get_db_manager()
        session_dir = self._get_session_directory(user_id, session_id, self.results_path)
        saved_files = {}
        
        # 전체 보고서 저장
        if "full_report" in analysis_result:
            report_filename = f"full_report_{session_id}.md"
            report_path = session_dir / report_filename
            
            async with aiofiles.open(report_path, 'w', encoding='utf-8') as f:
                await f.write(analysis_result["full_report"])
            
            saved_files["full_report"] = {
                "filename": report_filename,
                "file_path": str(report_path),
                "file_size": len(analysis_result["full_report"].encode('utf-8'))
            }
        
        # 섹션별 파일 저장
        sections = analysis_result.get("sections", {})
        for section_name, section_content in sections.items():
            if section_content:
                section_filename = f"{section_name}_{session_id}.html"
                section_path = session_dir / section_filename
                
                async with aiofiles.open(section_path, 'w', encoding='utf-8') as f:
                    await f.write(section_content)
                
                saved_files[section_name] = {
                    "filename": section_filename,
                    "file_path": str(section_path),
                    "file_size": len(section_content.encode('utf-8'))
                }
        
        # 데이터베이스에 분석 결과 저장
        await db_manager.save_analysis_result(session_id, user_id, analysis_result)
        
        return saved_files
    
    async def get_user_files(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """사용자의 모든 파일 정보 조회"""
        db_manager = get_db_manager()
        
        # 사용자의 세션 목록 조회
        sessions = await db_manager.get_user_sessions(user_id)
        
        user_files = {
            "sessions": [],
            "total_sessions": len(sessions)
        }
        
        for session in sessions:
            session_info = {
                "session_id": session["id"],
                "session_name": session["session_name"],
                "created_at": session["created_at"],
                "image_count": session["image_count"],
                "status": session["analysis_status"],
                "has_feedback": bool(session.get("feedback")),
                "feedback_rating": session.get("feedback_rating")
            }
            user_files["sessions"].append(session_info)
        
        return user_files
    
    async def cleanup_old_files(self, days_old: int = 30):
        """오래된 파일들 정리 (선택적 기능)"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # 구현 예정: 오래된 파일들을 찾아서 삭제
        # 실제 운영에서는 더 정교한 정리 로직이 필요
        pass
    
    def get_file_path(self, user_id: str, session_id: str, filename: str) -> Optional[Path]:
        """파일 경로 조회"""
        session_dir = self._get_session_directory(user_id, session_id, self.results_path)
        file_path = session_dir / filename
        
        if file_path.exists():
            return file_path
        return None

# 전역 파일 저장 매니저
file_storage_manager = None

def get_file_storage_manager() -> FileStorageManager:
    global file_storage_manager
    if file_storage_manager is None:
        file_storage_manager = FileStorageManager()
    return file_storage_manager
