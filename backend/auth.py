import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_db_manager, DatabaseManager

# 보안 설정
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7일

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 토큰 보안
security = HTTPBearer()

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        print(f"비밀번호 검증: '{plain_password}' vs '{hashed_password}'")
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"비밀번호 검증 결과: {result}")
        return result
    
    def get_password_hash(self, password: str) -> str:
        """비밀번호 해싱"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """JWT 액세스 토큰 생성"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """JWT 토큰 검증"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return {"username": username}
        except JWTError:
            return None
    
    async def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """사용자 인증"""
        print(f"사용자 인증 시도: {username}")
        
        user = await self.db_manager.get_user_by_username(username)
        print(f"데이터베이스에서 조회된 사용자: {user}")
        
        if not user:
            print(f"사용자 '{username}'을 찾을 수 없습니다.")
            return None
            
        if not self.verify_password(password, user["password_hash"]):
            print(f"사용자 '{username}'의 비밀번호가 일치하지 않습니다.")
            return None
            
        print(f"사용자 '{username}' 인증 성공")
        return user
    
    async def register_user(self, username: str, email: str, password: str, 
                          full_name: str = None, organization: str = None) -> Dict[str, Any]:
        """새 사용자 등록"""
        # 사용자명 중복 확인
        existing_user = await self.db_manager.get_user_by_username(username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 사용자명입니다."
            )
        
        # 비밀번호 해싱
        hashed_password = self.get_password_hash(password)
        
        # 사용자 생성
        user = await self.db_manager.create_user(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            organization=organization
        )
        
        return user

# 전역 인증 매니저
auth_manager = None

def get_auth_manager() -> AuthManager:
    global auth_manager
    if auth_manager is None:
        db_manager = get_db_manager()
        auth_manager = AuthManager(db_manager)
    return auth_manager

# 의존성 함수들
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """현재 로그인한 사용자 정보 가져오기"""
    auth_mgr = get_auth_manager()
    token_data = auth_mgr.verify_token(credentials.credentials)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 정보입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await auth_mgr.db_manager.get_user_by_username(token_data["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """현재 활성 사용자 확인"""
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="비활성 사용자입니다."
        )
    return current_user

# 베타 테스터용 기본 사용자 생성 함수
async def create_beta_testers():
    """베타 테스터 기본 계정 생성"""
    auth_mgr = get_auth_manager()
    
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
    
    created_users = []
    for tester in beta_testers:
        try:
            user = await auth_mgr.register_user(**tester)
            created_users.append(user)
            print(f"베타 테스터 생성됨: {tester['username']}")
        except HTTPException as e:
            if "이미 존재하는 사용자명" in str(e.detail):
                print(f"베타 테스터 이미 존재: {tester['username']}")
            else:
                print(f"베타 테스터 생성 실패: {tester['username']} - {e.detail}")
    
    return created_users
