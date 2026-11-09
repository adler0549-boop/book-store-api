from math import ceil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from ..database import get_db
from ..models import Book, Author, Genre
from ..schemas import (
    BookCreate,
    BookResponse,
    PaginatedBooks
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# ==========================================
# GET /books
#
# Примеры:
#
# /books
# /books?page=1&per_page=5
# /books?search=Harry
# /books?genre=Fantasy
# /books?search=Harry&genre=Fantasy
# ==========================================

@router.get(
    "/",
    response_model=PaginatedBooks
)
def get_books(
    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),

    per_page: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of books per page"
    ),

    search: str | None = Query(
        None,
        description="Search by book title"
    ),

    genre: str | None = Query(
        None,
        description="Filter by genre"
    ),

    db: Session = Depends(get_db)
):

    query = db.query(Book)

    # ======================================
    # Поиск по названию
    # ======================================

    if search:
        query = query.filter(
            Book.title.ilike(f"%{search}%")
        )

    # ======================================
    # Фильтрация по жанру
    # ======================================

    if genre:
        query = query.join(
            Book.genres
        ).filter(
            Genre.name.ilike(genre)
        )

    # ======================================
    # Общее количество книг
    # ======================================

    total = query.distinct().count()

    # ======================================
    # Пагинация
    # ======================================

    offset = (page - 1) * per_page

    books = (
        query
        .options(
            joinedload(Book.author),
            joinedload(Book.genres)
        )
        .distinct()
        .offset(offset)
        .limit(per_page)
        .all()
    )

    pages = ceil(total / per_page) if total else 0

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages,
        "books": books
    }


# ==========================================
# GET /books/{book_id}
# ==========================================

@router.get(
    "/{book_id}",
    response_model=BookResponse
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = (
        db.query(Book)
        .options(
            joinedload(Book.author),
            joinedload(Book.genres)
        )
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# ==========================================
# POST /books
# ==========================================

@router.post(
    "/",
    response_model=BookResponse,
    status_code=201
)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
):

    # ======================================
    # Проверяем автора
    # ======================================

    author = db.query(Author).filter(
        Author.id == book_data.author_id
    ).first()

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    # ======================================
    # Получаем жанры
    # ======================================

    genres = db.query(Genre).filter(
        Genre.id.in_(book_data.genre_ids)
    ).all()

    if len(genres) != len(set(book_data.genre_ids)):
        raise HTTPException(
            status_code=404,
            detail="One or more genres not found"
        )

    # ======================================
    # Создаём книгу
    # ======================================

    book = Book(
        title=book_data.title,
        description=book_data.description,
        price=book_data.price,
        year=book_data.year,
        author_id=book_data.author_id
    )

    book.genres = genres

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


# ==========================================
# PUT /books/{book_id}
# ==========================================

@router.put(
    "/{book_id}",
    response_model=BookResponse
)
def update_book(
    book_id: int,
    book_data: BookCreate,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # ======================================
    # Проверяем автора
    # ======================================

    author = db.query(Author).filter(
        Author.id == book_data.author_id
    ).first()

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    # ======================================
    # Проверяем жанры
    # ======================================

    genres = db.query(Genre).filter(
        Genre.id.in_(book_data.genre_ids)
    ).all()

    if len(genres) != len(set(book_data.genre_ids)):
        raise HTTPException(
            status_code=404,
            detail="One or more genres not found"
        )

    # ======================================
    # Обновляем книгу
    # ======================================

    book.title = book_data.title
    book.description = book_data.description
    book.price = book_data.price
    book.year = book_data.year
    book.author_id = book_data.author_id
    book.genres = genres

    db.commit()
    db.refresh(book)

    return book


# ==========================================
# DELETE /books/{book_id}
# ==========================================

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }