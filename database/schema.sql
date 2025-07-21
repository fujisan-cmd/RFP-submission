-- たんたんアプリ データベーススキーマ（更新版）

-- データベース作成
CREATE DATABASE IF NOT EXISTS tantan_app
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tantan_app;

-- usersテーブル（更新版）
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ユーザー管理ID（一意の整数値通し番号）',
    email VARCHAR(50) UNIQUE NOT NULL COMMENT 'メールアドレス',
    hashed_pw VARCHAR(100) NOT NULL COMMENT 'ハッシュ化されたパスワード',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
    last_login DATETIME COMMENT '最終ログイン日時',
    failed_login_counts INT DEFAULT 0 COMMENT 'ログイン試行失敗数',
    lock_until DATETIME COMMENT 'ロック解除の時刻'
) COMMENT 'ユーザー情報テーブル';

-- sessionsテーブル（新規追加）
CREATE TABLE sessions (
    session_id VARCHAR(100) PRIMARY KEY COMMENT 'セッション管理ID',
    user_id INT NOT NULL COMMENT 'ユーザーID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'セッション作成時刻',
    expires_at DATETIME NOT NULL COMMENT 'セッション有効期限',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'ログイン状態管理',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
) COMMENT 'セッション管理テーブル';

-- ログイン試行履歴テーブル（Want要件：アカウントロック用）
CREATE TABLE login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT COMMENT 'ユーザーID',
    attempt_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '試行時刻',
    success BOOLEAN DEFAULT FALSE COMMENT '成功フラグ',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    INDEX idx_user_id_time (user_id, attempt_time)
) COMMENT 'ログイン試行履歴テーブル';