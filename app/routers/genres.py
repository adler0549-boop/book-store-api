from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Genre
from ..schemas import GenreCreate, GenreResponse


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


# ==========================================
# GET /genres
# ==========================================

@router.get("/", response_model=list[GenreResponse])
def get_genres(
    db: Session = Depends(get_db)
):

    genres = db.query(Genre).all()

    return genres


# ==========================================
# GET /genres/{genre_id}
# ==========================================

@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):

    genre = db.query(Genre).filter(
        Genre.id == genre_id
    ).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    return genre


# ==========================================
# POST /genres
# ==========================================

@router.post(
    "/",
    response_model=GenreResponse,
    status_code=201
)
def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db)
):

    existing_genre = db.query(Genre).filter(
        Genre.name == genre_data.name
    ).first()

    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="Genre already exists"
        )

    genre = Genre(
        name=genre_data.name
    )

    db.add(genre)
    db.commit()
    db.refresh(genre)

    return genre


# ==========================================
# DELETE /genres/{genre_id}
# ==========================================

@router.delete("/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):

    genre = db.query(Genre).filter(
        Genre.id == genre_id
    ).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    db.delete(genre)
    db.commit()

    return {
        "message": "Genre deleted successfully"
    }