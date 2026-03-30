from fastapi import FastAPI
from src.books.routes import book_router
from src.users.routes import user_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.middleware import register_middleware
from fastapi.openapi.models import Contact
@asynccontextmanager
async def life_span(app : FastAPI):
    print("server is starting ... ")
    await init_db()
    yield 
    print("Server has been stopped")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact=Contact(
        name = "Begzod Turdibekov",
        email="begzodasidev@gmail.com"
    )
)   

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags = ['Books'])
app.include_router(user_router, prefix=f"/api/{version}/users", tags = ['Users'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags = ['Reviews'])