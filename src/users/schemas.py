from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from src.books.schemas import BookCreateModel

class UserCreateModel(BaseModel):
    first_name : str = Field(max_length=50)
    last_name : str = Field(max_length=50)
    username : str = Field(..., min_length=3, max_length=30)
    email : EmailStr
    password : str = Field(..., min_length=8, max_length=64)

class UserModel:
    uid : int
    username : str
    email : str
    first_name : str
    last_name : str
    is_verified : bool
    password_hash : str
    created_at : datetime
    updated_at : datetime
    role : str
    

    class Config:
        from_attributes = True

class UserBooksModel(UserModel):
    books : list[BookCreateModel]



class UserLoginModel(BaseModel):
    email : EmailStr
    password : str = Field(..., min_length=8, max_length=64)

class UserRead(BaseModel):
    username : str
    role : str

class EmailModel(BaseModel):
    addresses : list[str]

class PasswordResetRequestModel(BaseModel):
    email : str

class PasswordResetConfirmModel(BaseModel):
    new_password : str
    confirm_new_password : str
