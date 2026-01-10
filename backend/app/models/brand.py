"""
Brand model
ブランド情報を管理
"""

from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Brand(Base):
    """ブランドモデル"""
    __tablename__ = "brands"

    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # ブランド情報
    name = Column(String(200), unique=True, nullable=False, index=True)
    name_kana = Column(String(200), nullable=True)
    logo_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    official_site_url = Column(String(500), nullable=True)
    rakuten_brand_id = Column(String(100), nullable=True, index=True)

    # 状態
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    # タイムスタンプ
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="brand")

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"
