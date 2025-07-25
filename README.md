# ConceptCraft by たんたん - ログイン機能MVP

大企業における新規事業開発担当者を対象としたWebアプリケーションのログイン機能実装です。

## 技術スタック

- **フロントエンド**: Next.js 15.4.2 + React + TypeScript + Tailwind CSS
- **バックエンド**: FastAPI + Python
- **データベース**: MySQL
- **認証**: HttpOnly Cookie + セッション管理

## セットアップ

### 前提条件
- Node.js 18以上
- Python 3.8以上
- MySQL 8.0以上

### データベース設定

1. MySQLにデータベースを作成:
```sql
CREATE DATABASE tantan_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. スキーマを適用:
```bash
mysql -u root -p tantan_app < database/schema.sql
```

### バックエンド起動

1. 依存関係をインストール:
```bash
cd backend
pip install -r requirements.txt
```

2. 環境変数を設定 (`.env`ファイル):
```env
# データベース設定
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=tantan_app

# セキュリティ設定
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

3. サーバーを起動:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### フロントエンド起動

1. 依存関係をインストール:
```bash
cd frontend
npm install
```

2. 開発サーバーを起動:
```bash
npm run dev
```

## アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API仕様書**: http://localhost:8000/docs

## 主要機能

### 新規登録 (`/signup`)
- メールアドレス（一意性確認）
- パスワード（半角英数字+記号、8文字以上、記号必須）
- パスワード確認
- ハニーポット（ボット対策）
- 登録完了ポップアップ

### ログイン (`/login`)
- メールアドレス・パスワード認証
- HttpOnly Cookie セッション管理
- レート制限（15分に5回まで）
- アカウントロック（3回失敗で5分間）
- 自動ログアウト（15分間非操作）

### セキュリティ機能
- パスワードハッシュ化（bcrypt）
- セッション管理
- SQLインジェクション対策
- CORS設定
- レート制限・アカウントロック

## APIエンドポイント

- `POST /api/signup` - 新規登録
- `POST /api/login` - ログイン
- `POST /api/logout` - ログアウト
- `GET /api/auth/me` - 現在のユーザー情報取得
- `GET /health` - ヘルスチェック

## 重要な修正内容

### MySQL互換性問題の解決
- PyMySQLからmysqlclient（MySQLdb）に変更
- MySQL 8.0の`caching_sha2_password`認証に対応

### 環境変数の適切な読み込み
- `python-dotenv`による`.env`ファイル読み込み

### エラーハンドリングの強化
- データベース接続エラーの適切な処理
- 詳細なエラーメッセージ

## トラブルシューティング

### データベース接続エラー
```
(1049, "Unknown database 'tantan_app'")
```
- データベースが作成されていることを確認
- `.env`ファイルの設定を確認
- MySQLサーバーが起動していることを確認

### 認証エラー
```
(1045, "Access denied for user...")
```
- MySQL認証情報を確認
- 必要に応じてユーザー権限を付与

## ライセンス

このプロジェクトは株式会社たんたん×すするの開発依頼に基づいて作成されました。