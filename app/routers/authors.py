from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Author
from ..schemas import AuthorCreate, AuthorResponse


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


# ==========================================
# GET /authors
# ==========================================

@router.get("/", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):

    authors = db.query(Author).all()

    return authors


# ==========================================
# GET /authors/{author_id}
# ==========================================

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):

    author = db.query(Author).filter(
        Author.id == author_id
    ).first()

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author


# ==========================================
# POST /authors
# ==========================================

@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=201
)
def create_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db)
):

    author = Author(
        name=author_data.name
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


# ==========================================
# DELETE /authors/{author_id}
# ==========================================

@router.delete("/{author_id}")
def delete_author(
    author_id: int,
    db: Session = Depends(get_db)
):

    author = db.query(Author).filter(
        Author.id == author_id
    ).first()

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    db.delete(author)
    db.commit()

    return {
        "message": "Author deleted successfully"
    }