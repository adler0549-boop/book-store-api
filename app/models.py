from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship

from .database import Base


# ==========================================
# Many-to-Many таблица Book <-> Genre
# ==========================================

book_genres = Table(
    "book_genres",
    Base.metadata,

    Column(
        "book_id",
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "genre_id",
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True
    ),
)


# ==========================================
# Author
# ==========================================

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )


# ==========================================
# Genre
# ==========================================

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    books = relationship(
        "Book",
        secondary=book_genres,
        back_populates="genres"
    )


# ==========================================
# Book
# ==========================================

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False,
        index=True
    )

    description = Column(
        String(1000),
        nullable=True
    )

    price = Column(
        Float,
        nullable=False
    )

    year = Column(
        Integer,
        nullable=True
    )

    author_id = Column(
        Integer,
        ForeignKey("authors.id"),
        nullable=False
    )

    # Many-to-One
    author = relationship("Author", back_populates="books")

    # Many-to-Many
    genres = relationship("Genre", secondary=book_genres, back_populates="books")