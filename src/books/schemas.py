from pydantic import BaseModel
from datetime import datetime,date
from uuid import UUID

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date | None = None
    page_count: int
    language: str
    created_at : datetime
    updated_at : datetime
    user_uid : UUID | None = None


class BookCreateModel(BaseModel):
    user_uid : UUID | None = None
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: date | None = None

class BookUpdateModel(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None
    published_date: date | None = None

class BookRead(BaseModel):
    title : str 
    author : str