from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True
    )
    username: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    full_name: Mapped[str] = mapped_column(
        String(200), default=""
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class AppListing(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, default="")
    risk_status: Mapped[str] = mapped_column(
        String(50), default="Unverified"
    )
    launch_date: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class Loot(Base):
    __tablename__ = "loots"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(Text)
    end_date: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="Active"
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class PromotionRequest(Base):
    __tablename__ = "promotion_requests"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    service_type: Mapped[str] = mapped_column(String(100))
    details: Mapped[str] = mapped_column(Text)
    budget: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(
        String(50), default="Pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
