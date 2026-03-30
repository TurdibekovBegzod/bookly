from src.db.main import Base
from sqlalchemy import String, Column, DateTime, Boolean, Integer, UUID, Date, ForeignKey
from sqlalchemy.orm import Relationship, Mapped
from datetime import datetime, timezone
import uuid




class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=200))
    author = Column(String(length=200))
    publisher = Column(String(length=200))
    published_date = Column(Date)
    page_count = Column(Integer)
    user_uid = Column(UUID(as_uuid=True), ForeignKey('users.uid'), default=None)
    language = Column(String(length=20))
    user  : Mapped["User"]= Relationship(back_populates='books')
    reviews : Mapped[list['Review']] = Relationship(back_populates='book', lazy='selectin')
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda : datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda : datetime.now(timezone.utc), 
        onupdate=lambda : datetime.now(timezone.utc))

    def __str__(self):
        return f"<Book with name {self.title}"

class User(Base):
    __tablename__ = 'users'
    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(length=30), nullable=False)
    email = Column(String(length=200), nullable=False)
    first_name = Column(String(length=50), nullable = True)
    last_name = Column(String(length=50), nullable = True)
    role = Column(String(length=30), nullable = False, default="user")
    is_verified = Column(Boolean, default=False)
    password_hash = Column(String, nullable=False) 
    books : Mapped[list["Book"]] = Relationship(back_populates="user", lazy='selectin')
    reviews : Mapped[list["Review"]] = Relationship(back_populates="user", lazy='selectin')
    created_at = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda : datetime.now(timezone.utc),
        onupdate=lambda : datetime.now(timezone.utc)
    )

    def __str__(self):
        return f"<User with name {self.first_name} and lastname {self.last_name}"
    
class Review(Base):
    __tablename__ = "reviews"
    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_uid = Column(UUID(as_uuid=True), ForeignKey('users.uid'), default=None)
    book_id = Column(Integer, ForeignKey('books.id'), default=None)
    rating = Column(Integer)
    review_text = Column(String)
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda : datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda : datetime.now(timezone.utc), 
        onupdate=lambda : datetime.now(timezone.utc))
    
    user : Mapped['User'] = Relationship(back_populates='reviews')
    book : Mapped['Book'] = Relationship(back_populates='reviews')

    def __str__(self):
        return f"<Review for {self.book_id} by {self.user_uid}"
    