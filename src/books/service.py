from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from sqlalchemy import select, update, delete
from src.db.models import Book


class BookService:
    async def get_all_books(self, db : AsyncSession):
        query = select(Book)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_book(self, book_id : int, db : AsyncSession) -> Book:
        query = select(Book).where(Book.id == book_id)
        result = await db.execute(query)
        return result.scalars().first()


    async def create_book(self, book_data : BookCreateModel, db : AsyncSession):
        book = Book(**book_data.model_dump())
        db.add(book)
        await db.commit()
        await db.refresh(book)

        return book

    async def update_book(self, book_id : int, book_data : BookUpdateModel, db : AsyncSession):
        query = update(Book).where(Book.id == book_id).values(**book_data.model_dump(exclude_unset=True)).returning(Book)
        result = await db.execute(query)

        await db.commit()

        return result.scalars().one()

    async def delete_book(self, book_id : int, db : AsyncSession):
        query = delete(Book).where(Book.id == book_id)
        await db.execute(query)

        await db.commit()
        
    async def get_user_books(self, user_uid, db : AsyncSession):
        query = select(Book).where(Book.user_uid == user_uid)
        result = await db.execute(query)
        return result.scalars().all()
