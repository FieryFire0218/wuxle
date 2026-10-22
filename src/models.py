from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Novel(Base):
    __tablename__ = "novels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    translator: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    chapters: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    genres: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "author": self.author,
            "translator": self.translator,
            "rating": self.rating,
            "chapters": self.chapters,
            "genres": self.genres,
        }


class DailyAnswer(Base):
    __tablename__ = "daily_answers"

    day: Mapped[date] = mapped_column(
        Date,
        primary_key=True,
    )

    novel_id: Mapped[int] = mapped_column(
        ForeignKey("novels.id", ondelete="RESTRICT"),
        nullable=False,
    )

    answer_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

