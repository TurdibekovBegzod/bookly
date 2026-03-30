from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_db
from src.users.utils import decode_access_token
from src.users.service import UserService
from src.users.schemas import UserModel


user_service = UserService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

async def get_current_user(
        token : str = Depends(oauth2_scheme),
        db : AsyncSession = Depends(get_db)
):
    user_dict = decode_access_token(token)

    

    email = user_dict['user']['email']

    user = await user_service.get_user_by_email(email, db)

    return user


class RoleChecker:
    def __init__(self, allowed_roles : list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user : UserModel = Depends(get_current_user)) -> bool:
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your email is not verified yet!"
            )

        if user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your role is not permitted to perform this action"
        )
