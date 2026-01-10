"""
Watchlist model
ユーザーが追跡している商品を管理
"""

from sqlalchemy import Column, BigInteger, Numeric, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Watchlist(Base):
    """ウォッチリストモデル"""
    __tablename__ = "watchlists"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 外部キー
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # 価格追跡設定
    target_price = Column(Numeric(10, 2), nullable=True)
    initial_price = Column(Numeric(10, 2), nullable=False)
    lowest_price = Column(Numeric(10, 2), nullable=True)

    # 通知状態
    is_notified = Column(Boolean, nullable=False, default=False, index=True)
    last_notified_at = Column(DateTime, nullable=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="watchlists")
    product = relationship("Product", back_populates="watchlists")
    notifications = relationship("Notification", back_populates="watchlist")

    # 複合インデックス（ユニーク制約: 1ユーザー1商品は1回のみ登録可能）
    __table_args__ = (
        Index('idx_watchlists_user_product', 'user_id', 'product_id', unique=True),
        Index('idx_watchlists_user_recent', 'user_id', 'created_at'),
    )

    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, target_price={self.target_price})>"
