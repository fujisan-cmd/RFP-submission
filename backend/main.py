from fastapi import FastAPI, HTTPException, Depends, Cookie, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Optional
from dotenv import load_dotenv
import logging
import os

# .envファイルを読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from models import UserCreate, UserLogin, AuthResponse, ErrorResponse, UserResponse
from user_service import UserService, SessionService
from rate_limiter import RateLimiter

app = FastAPI(title="ConceptCraft by tantan API")

# CORS設定（環境変数から取得、デフォルト値設定）
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001").split(",")
logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "ConceptCraft by tantan API へようこそ！"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.post("/api/signup", response_model=AuthResponse)
async def signup(user_data: UserCreate, request: Request):
    """新規ユーザー登録"""
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"Signup attempt from {client_ip} for email: {user_data.email}")
    
    try:
        result = UserService.create_user(user_data.email, user_data.password)
        
        if result["success"]:
            logger.info(f"Successful signup for email: {user_data.email}")
            return AuthResponse(message=result["message"])
        else:
            logger.warning(f"Failed signup for email: {user_data.email} - {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error for {user_data.email}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"サーバーエラーが発生しました: {str(e)}")

@app.post("/api/login", response_model=AuthResponse)
async def login(user_data: UserLogin, response: Response, request: Request):
    """ユーザーログイン"""
    client_ip = RateLimiter.get_client_ip(request)
    
    # レート制限チェック（ログインは15分に5回まで）
    rate_check = RateLimiter.check_rate_limit(client_ip, "login", limit=5, window_minutes=15)
    if not rate_check["allowed"]:
        raise HTTPException(
            status_code=429, 
            detail=f"ログイン試行回数が制限を超えました。{rate_check['reset_time'].strftime('%H:%M')}以降に再試行してください"
        )
    
    result = UserService.authenticate_user(user_data.email, user_data.password)
    
    # 試行を記録
    user_id = result.get("user", {}).get("user_id") if result["success"] else None
    RateLimiter.record_attempt(client_ip, user_id=user_id, success=result["success"])
    
    if result["success"]:
        # セッションを作成
        session_id = SessionService.create_session(result["user"]["user_id"])
        
        if not session_id:
            raise HTTPException(status_code=500, detail="セッション作成に失敗しました")
        
        # HttpOnly CookieにセッションIDを設定
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=15 * 60,  # 15分
            samesite="lax",
            secure=False  # 開発環境ではFalse、本番環境ではTrue
        )
        
        return AuthResponse(
            message=result["message"],
            user=UserResponse(
                user_id=result["user"]["user_id"],
                email=result["user"]["email"],
                created_at=result["user"]["created_at"]
            )
        )
    else:
        raise HTTPException(status_code=401, detail=result["message"])

@app.post("/api/logout")
async def logout(response: Response, session_id: Optional[str] = Cookie(None)):
    """ログアウト"""
    if session_id:
        SessionService.invalidate_session(session_id)
    
    response.delete_cookie(key="session_id")
    return {"message": "ログアウトしました"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user(session_id: Optional[str] = Cookie(None)):
    """現在のユーザー情報を取得"""
    if not session_id:
        raise HTTPException(status_code=401, detail="認証が必要です")
    
    user_id = SessionService.validate_session(session_id)
    if not user_id:
        raise HTTPException(status_code=401, detail="無効なセッションです")
    
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        last_login=user["last_login"]
    )