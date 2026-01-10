"""
Category model
商品カテゴリーを管理（階層構造対応）
"""

from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Category(Base):
    """カテゴリーモデル"""
    __tablename__ = "categories"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # カテゴリー情報
    name = Column(String(200), nullable=False)
    name_kana = Column(String(200), nullable=True)

    # 階層構造
    parent_id = Column(BigInteger, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)

    # 表示設定
    display_order = Column(Integer, nullable=False, default=0, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships (self-referential)
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"
