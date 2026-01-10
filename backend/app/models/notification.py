"""
Notification model
ユーザーへの通知履歴を管理
"""

from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Notification(Base):
    """通知モデル"""
    __tablename__ = "notifications"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 外部キー
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    watchlist_id = Column(BigInteger, ForeignKey("watchlists.id", ondelete="SET NULL"), nullable=True, index=True)

    # 通知内容
    notification_type = Column(String(50), nullable=False)  # price_drop, target_reached, weekly_ranking, stock_alert
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_metadata = Column("metadata", JSON, nullable=True)  # Use column name 'metadata' in DB, but attribute name 'notification_metadata' in Python

    # 通知状態
    is_read = Column(Boolean, nullable=False, default=False, index=True)
    sent_at = Column(DateTime, nullable=True, index=True)
    read_at = Column(DateTime, nullable=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")
    watchlist = relationship("Watchlist", back_populates="notifications")

    # 複合インデックス
    __table_args__ = (
        Index('idx_notifications_unread', 'user_id', 'is_read', 'sent_at'),
    )

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.notification_type}', is_read={self.is_read})>"
