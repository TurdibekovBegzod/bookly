from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel, Book
from src.books.service import BookService
from src.db.main import get_db
from src.users.dependencies import RoleChecker, get_current_user
from src.users.schemas import UserModel

book_router = APIRouter()
book_service = BookService()
role_checker = Depends(RoleChecker(['admin', 'user']))


@book_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(
    book_data : BookCreateModel, 
    db : AsyncSession = Depends(get_db),
    user_data : UserModel = Depends(get_current_user)
):
    

    book_data.user_uid = user_data.uid
    return await book_service.create_book(book_data=book_data, db = db)
    

@book_router.get("/user/{user_uid}", response_model=list[Book], dependencies=[role_checker])
async def get_user_books(user_uid, db : AsyncSession = Depends(get_db)):
    books = await book_service.get_user_books(user_uid, db)

    return books

@book_router.get("/", response_model=list[Book], dependencies=[role_checker])
async def get_all_books(db : AsyncSession = Depends(get_db)):
    books = await book_service.get_all_books(db)

    return books


@book_router.get("/{book_id}", response_model = Book, dependencies=[role_checker])
async def get_book(book_id : int = 1, db : AsyncSession = Depends(get_db)):
    return await book_service.get_book(book_id,db)


@book_router.patch("/{book_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Book, dependencies=[role_checker])
async def update_book(book_id : int, book_data : BookUpdateModel, db : AsyncSession = Depends(get_db)):
    return await book_service.update_book(book_id, book_data, db)

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_id : int, db : AsyncSession = Depends(get_db)):
    await book_service.delete_book(book_id, db)