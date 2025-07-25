# ConceptCraft Backend API

株式会社たんたん×すする 新規事業開発支援アプリケーション バックエンドAPI

## 🚀 セットアップ手順

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. データベースセットアップ
```bash
# MySQLサーバーに接続して以下のSQLを実行
CREATE DATABASE tantan_app;
USE tantan_app;

# テーブル作成（schema.sqlを実行）
```

### 3. サーバー起動
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔒 セキュリティ設定について

### デフォルト値について
このアプリケーションはデフォルト値として以下を含んでいます：
- **DB_PASSWORD**: `"password"`
- **DB_USER**: `"root"`

**これは開発・テスト環境での利便性のためです**

### セキュリティベストプラクティス

#### ✅ 実装済みセキュリティ対策
- 環境変数による設定管理
- パスワードハッシュ化（bcrypt）
- HttpOnly Cookie認証
- SQLインジェクション対策
- レート制限（ログイン試行）
- CORS設定

#### 🔧 本番環境での推奨設定

**1. 環境変数ファイルの作成**
```bash
cp .env.example .env
```

**2. 実際の値に変更**
```bash
# .envファイルを編集
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=your_db_name
SECRET_KEY=your_256_bit_secret_key
```

**3. 推奨パスワード要件**
- 12文字以上
- 大文字・小文字・数字・記号を含む
- 辞書攻撃に耐えうる複雑性

**4. データベースユーザー**
```sql
-- 専用ユーザーの作成例
CREATE USER 'conceptcraft_app'@'localhost' IDENTIFIED BY 'very_secure_password_123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON tantan_app.* TO 'conceptcraft_app'@'localhost';
FLUSH PRIVILEGES;
```

## 🛡️ セキュリティ監査項目

### チェックリスト
- [ ] デフォルトパスワードを変更済み
- [ ] 専用データベースユーザーを作成済み
- [ ] `.env`ファイルがGitに含まれていない
- [ ] 秘密鍵（SECRET_KEY）をランダム生成済み
- [ ] データベース接続がSSL/TLS暗号化済み（必要に応じて）

### 設定確認コマンド
```bash
# 現在の設定を確認
curl http://localhost:8000/health/detailed

# デバッグ情報（パスワードは表示されません）
curl http://localhost:8000/debug/info
```

## 📊 API エンドポイント

### 基本情報
- **Base URL**: `http://localhost:8000`
- **認証方式**: HttpOnly Cookie

### エンドポイント一覧

| Method | Endpoint | 説明 |
|--------|----------|------|
| GET | `/` | API基本情報 |
| GET | `/health` | 基本ヘルスチェック |
| GET | `/health/detailed` | 詳細ヘルスチェック |
| GET | `/debug/info` | デバッグ情報 |
| POST | `/api/signup` | 新規ユーザー登録 |
| POST | `/api/signup/simple` | シンプル登録テスト |
| POST | `/api/login` | ユーザーログイン |
| POST | `/api/logout` | ログアウト |
| GET | `/api/auth/me` | 現在のユーザー情報 |

## 🔍 トラブルシューティング

### 500エラーが発生する場合

1. **詳細ヘルスチェック**
   ```bash
   curl http://localhost:8000/health/detailed
   ```

2. **シンプルテスト**
   ```bash
   curl -X POST http://localhost:8000/api/signup/simple \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "TestPass123#"}'
   ```

3. **ログ確認**
   - バックエンドコンソールで詳細エラーログを確認

### よくある問題と解決策

| 問題 | 原因 | 解決策 |
|------|------|--------|
| データベース接続エラー | MySQL未起動 | MySQLサーバーを起動 |
| MySQL 8.0認証エラー | caching_sha2_password | 下記の「MySQL 8.0認証対応」参照 |
| CORS エラー | オリジン設定 | `ALLOWED_ORIGINS`を確認 |
| 認証エラー | Cookie設定 | ブラウザのCookie設定確認 |

## 🔧 MySQL 8.0認証対応

### 認証エラーが発生する場合
```
Authentication plugin 'caching_sha2_password' cannot be loaded
```

### 解決方法1: ユーザー認証方式の変更（推奨）
```sql
-- MySQLにrootでログイン
mysql -u root -p

-- 認証方式を変更
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

### 解決方法2: 新規ユーザー作成
```sql
-- 専用ユーザーを作成
CREATE USER 'conceptcraft'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON tantan_app.* TO 'conceptcraft'@'localhost';
FLUSH PRIVILEGES;

-- .envファイルで設定
DB_USER=conceptcraft
DB_PASSWORD=secure_password
```

### 解決方法3: PyMySQLバージョン確認
```bash
# 最新版を使用（1.1.1以降推奨）
pip install PyMySQL==1.1.1
```

## 📁 ファイル構成

```
backend/
├── main.py              # FastAPIアプリケーション
├── database.py          # データベース接続
├── user_service.py      # ユーザー関連ビジネスロジック
├── auth.py             # 認証・パスワードハッシュ
├── models.py           # データモデル
├── rate_limiter.py     # レート制限
├── requirements.txt    # 依存関係
├── .env.example       # 環境変数テンプレート
├── .env              # 実際の環境変数（Git除外）
└── README.md         # このファイル
```

## 🤝 サポート

技術的な質問や問題が発生した場合は、以下の情報と共にお問い合わせください：

1. エラーメッセージ
2. `/health/detailed`の出力
3. `/debug/info`の出力
4. 実行環境（OS、Pythonバージョン等）