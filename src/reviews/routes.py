from fastapi import APIRouter, Depends, status
from src.users.dependencies import get_db, get_current_user
from src.db.models import User
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.reviews.service import ReviewService
from src.users.schemas import UserModel
review_router = APIRouter()

review_service = ReviewService()

@review_router.post("/review/{book_id}", response_model = ReviewModel)
async def add_review_to_book(
    book_id : int,
    review_data : ReviewCreateModel,
    current_user : UserModel = Depends(get_current_user),
    db : AsyncSession =  Depends(get_db)
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_id = book_id,
        review_data = review_data,
        db = db
    )

    return new_review
