"""
WeeklyRanking model
AI生成の週次TOP10商品ランキングを管理
"""

from sqlalchemy import Column, BigInteger, Integer, Numeric, Date, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class WeeklyRanking(Base):
    """週次ランキングモデル"""
    __tablename__ = "weekly_rankings"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 外部キー
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # ランキング情報
    week_start_date = Column(Date, nullable=False, index=True)
    rank_position = Column(Integer, nullable=False)

    # スコアリング
    score = Column(Numeric(10, 4), nullable=False)
    watchlist_count = Column(Integer, nullable=False, default=0)
    price_drop_rate = Column(Numeric(5, 2), nullable=True)

    # AI生成コンテンツ
    ai_description = Column(Text, nullable=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="weekly_rankings")

    # 複合インデックス（ユニーク制約: 週ごとに同じ順位は1つのみ）
    __table_args__ = (
        Index('idx_weekly_rankings_week_rank', 'week_start_date', 'rank_position', unique=True),
        Index('idx_weekly_rankings_week', 'week_start_date', 'rank_position'),
    )

    def __repr__(self):
        return f"<WeeklyRanking(id={self.id}, week={self.week_start_date}, rank={self.rank_position}, product_id={self.product_id})>"
