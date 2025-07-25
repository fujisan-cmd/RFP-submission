import os
import MySQLdb as pymysql
from typing import Optional

class DatabaseConfig:
    """データベース設定クラス"""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.database = os.getenv("DB_NAME", "tantan_app")

class DatabaseConnection:
    """データベース接続クラス"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connection: Optional[pymysql.Connection] = None
    
    def connect(self) -> pymysql.Connection:
        """データベースに接続"""
        try:
            self._connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                passwd=self.config.password,
                db=self.config.database,
                charset='utf8mb4',
                connect_timeout=10
            )
            self._connection.autocommit(True)
            return self._connection
        except Exception as e:
            print(f"データベース接続エラー: {e}")
            raise
    
    def close(self):
        """データベース接続を閉じる"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def get_connection(self) -> pymysql.Connection:
        """接続を取得（接続されていない場合は新規接続）"""
        if not self._connection or not self._connection.open:
            return self.connect()
        return self._connection

# グローバルな設定とコネクション
db_config = DatabaseConfig()
db_connection = DatabaseConnection(db_config)