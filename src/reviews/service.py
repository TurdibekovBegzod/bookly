from src.db.models import Review
from src.users.service import UserService
from src.books.service import BookService
from src.reviews.schemas import ReviewCreateModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(self, user_email: str, book_id : int, review_data : ReviewCreateModel, db : AsyncSession ):
        try :
            book = await book_service.get_book(book_id = book_id, db=db)
            user = await user_service.get_user_by_email(email=user_email,db = db)

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            new_review.user = user
            new_review.book = book
            new_review.user_uid = user.uid
            new_review.book_id = book_id

            db.add(new_review)
            await db.commit()

            return new_review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops ... Something went wrong"
            )