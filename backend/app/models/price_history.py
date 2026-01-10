"""
PriceHistory model
商品の価格変動履歴を記録
"""

from sqlalchemy import Column, BigInteger, Numeric, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PriceHistory(Base):
    """価格履歴モデル"""
    __tablename__ = "price_histories"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 外部キー
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # 価格情報
    price = Column(Numeric(10, 2), nullable=False)
    is_on_sale = Column(Boolean, nullable=False, default=False)
    discount_rate = Column(Numeric(5, 2), nullable=True)

    # チェック日時
    checked_at = Column(DateTime, nullable=False, index=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="price_histories")

    # 複合インデックス
    __table_args__ = (
        Index('idx_price_histories_product_time', 'product_id', 'checked_at'),
    )

    def __repr__(self):
        return f"<PriceHistory(id={self.id}, product_id={self.product_id}, price={self.price}, checked_at={self.checked_at})>"
