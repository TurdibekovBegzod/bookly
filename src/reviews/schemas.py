from pydantic import BaseModel
from datetime import datetime
from src.users.schemas import UserRead
from src.books.schemas import BookRead
from pydantic import Field
import uuid


class ReviewModel(BaseModel):
    uid : uuid.UUID
    user_uid : uuid.UUID
    book_id  : int
    rating : int
    review_text : str
    created_at : datetime
    updated_at : datetime
    
    

class ReviewCreateModel(BaseModel):
    rating : int = Field(lt=5, gt=0)
    review_text : str
