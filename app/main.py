from fastapi import FastAPI
from .database import Base, engine
from .routers import books
from .routers import authors
from .routers import genres


# ==========================================
# Создание таблиц
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FastAPI
# ==========================================

app = FastAPI(
    title="Book Store API",
    description="Book Store API with FastAPI and SQLAlchemy ORM",
    version="1.0.0"
)


# ==========================================
# Routers
# ==========================================

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)


# ==========================================
# Главная страница
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Welcome to Book Store API",
        "docs": "/docs"
    }