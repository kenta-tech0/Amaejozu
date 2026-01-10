"""
User model
ユーザーアカウント情報を管理
"""

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """ユーザーモデル"""
    __tablename__ = "users"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 認証情報
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # プロフィール
    nickname = Column(String(100), nullable=True)

    # アカウント状態
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    # 通知設定
    notification_token = Column(String(500), nullable=True)
    email_notification_enabled = Column(Boolean, nullable=False, default=True)

    # ログイン履歴
    last_login_at = Column(DateTime, nullable=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    watchlists = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nickname='{self.nickname}')>"
