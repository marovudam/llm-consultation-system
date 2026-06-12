from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, DateTime

from app.db.base import Base

class User(Base):
    """Модель пользователя"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
