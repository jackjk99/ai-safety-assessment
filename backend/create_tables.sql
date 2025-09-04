-- Supabase 데이터베이스 테이블 생성 SQL
-- 이 파일의 내용을 Supabase 대시보드의 SQL Editor에서 실행하세요

-- 테이블 1: 사용자 테이블
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

-- 테이블 2: 분석 세션 테이블
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

-- 테이블 3: 업로드된 이미지 테이블
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

-- 테이블 4: 분석 파일 테이블
CREATE TABLE IF NOT EXISTS analysis_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES analysis_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_type VARCHAR(50) NOT NULL, -- 'risk_analysis', 'sgr_checklist', 'recommendations', 'full_report'
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_user_id ON analysis_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_uploaded_images_session_id ON uploaded_images(session_id);
CREATE INDEX IF NOT EXISTS idx_analysis_files_session_id ON analysis_files(session_id);
