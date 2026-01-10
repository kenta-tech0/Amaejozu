"""
Product model
商品情報を管理
"""

from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime, ForeignKey, Numeric, Integer, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Product(Base):
    """商品モデル"""
    __tablename__ = "products"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 楽天連携
    rakuten_item_code = Column(String(200), unique=True, nullable=False, index=True)
    rakuten_url = Column(String(500), nullable=False)
    affiliate_url = Column(String(500), nullable=True)

    # 商品情報
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    # 外部キー
    brand_id = Column(BigInteger, ForeignKey("brands.id", ondelete="SET NULL"), nullable=True, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)

    # 価格情報
    msrp_price = Column(Numeric(10, 2), nullable=True)
    current_price = Column(Numeric(10, 2), nullable=False, index=True)
    is_on_sale = Column(Boolean, nullable=False, default=False, index=True)
    discount_rate = Column(Numeric(5, 2), nullable=True)

    # レビュー情報
    review_average = Column(Numeric(3, 2), nullable=True, index=True)
    review_count = Column(Integer, nullable=False, default=0)

    # 在庫状態
    stock_status = Column(String(50), nullable=True)

    # メタデータ
    last_checked_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    watchlists = relationship("Watchlist", back_populates="product", cascade="all, delete-orphan")
    price_histories = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    weekly_rankings = relationship("WeeklyRanking", back_populates="product", cascade="all, delete-orphan")

    # 複合インデックス
    __table_args__ = (
        Index('idx_products_search', 'category_id', 'is_on_sale', 'current_price'),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', current_price={self.current_price})>"
