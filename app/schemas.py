from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# ==========================================
# Author schemas
# ==========================================

class AuthorCreate(BaseModel):
    name: str


class AuthorResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Genre schemas
# ==========================================

class GenreCreate(BaseModel):
    name: str


class GenreResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Book schemas
# ==========================================

class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    year: Optional[int] = None

    author_id: int
    genre_ids: List[int] = []


class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    year: Optional[int]

    author: AuthorResponse
    genres: List[GenreResponse]

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Pagination
# ==========================================

class PaginatedBooks(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int

    books: List[BookResponse]