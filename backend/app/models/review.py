"""
Review model
商品レビュー情報を管理
"""

from sqlalchemy import Column, BigInteger, String, Text, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Review(Base):
    """レビューモデル"""
    __tablename__ = "reviews"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 外部キー
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # 楽天連携
    rakuten_review_id = Column(String(100), unique=True, nullable=False, index=True)

    # レビュー情報
    reviewer_name = Column(String(100), nullable=True)
    rating = Column(Integer, nullable=False, index=True)
    review_text = Column(Text, nullable=True)
    helpful_count = Column(Integer, nullable=False, default=0)

    # レビュー日付
    review_date = Column(Date, nullable=False, index=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, product_id={self.product_id}, rating={self.rating})>"
