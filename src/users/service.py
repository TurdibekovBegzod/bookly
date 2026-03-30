from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import User
from .schemas import UserCreateModel, UserModel
from .utils import generate_password_hash

class UserService:
    
    async def get_user_by_email(self, email : str,  db : AsyncSession) -> UserModel:
        statement = select(User).where(User.email == email)
        result = await db.execute(statement)

        user = result.scalar_one_or_none()

        return user
    
    
    async def user_exists(self, email : str, db : AsyncSession):
        user = await self.get_user_by_email(email, db)
        if user:
            return True
        return False
    
    async def create_user(self, user_data : UserCreateModel, db : AsyncSession):
        user_data_dict = user_data.model_dump(exclude={"password"})

        new_user = User(**user_data_dict)


        new_user.password_hash = generate_password_hash(user_data.password)

        db.add(new_user)
        await db.commit()

        return new_user
    
    async def update_user(self, user: User, user_data : dict, db : AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)
        await db.commit()

        return user