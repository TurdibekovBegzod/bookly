from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from .schemas import UserCreateModel, UserBooksModel
from .service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_db
from src.users.utils import verify_password, create_access_token, decode_access_token, create_url_safe_token, decode_url_safe_token, generate_password_hash
from src.config import Config
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.users.dependencies import oauth2_scheme, get_current_user, RoleChecker
from fastapi.security import OAuth2PasswordRequestForm
from src.db.redis import add_jti_to_blocklist
from src.users.schemas import EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from src.celery_tasks import send_email
from src.config import Config

user_router= APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])




@user_router.post("/signup")
async def create_user_Account(user_data : UserCreateModel, bg_tasks : BackgroundTasks, db : AsyncSession = Depends(get_db)):
    email = user_data.email
    

    user_exists = await user_service.user_exists(email=email, db=db)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {email} already exists"
        )
    new_user = await user_service.create_user(user_data, db)

    token = create_url_safe_token({'email' : email})

    link = f"http://{Config.DOMAIN}:{Config.PORT}/api/v1/users/verify/{token}"
    
    body =f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href='{link}'>link</a> to verify your email</p>
"""
    
    emails = list(email)
    subject = "Welcome to our app"

    send_email.delay(emails, subject, body)
    

    return {
        "message":"Account Created! Check email to verify your account",
        "user" : new_user
    }

@user_router.get("/verify/{token}")
async def verify_user_account(token : str, db : AsyncSession = Depends(get_db)):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(email=user_email, db=db)

        if not user:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="User not found"
            )

        await user_service.update_user(user, {'is_verified': True}, db)
        

        return JSONResponse(
            content={
                "message" : "Account verified Successfully"
            },
            status_code = status.HTTP_200_OK
        )
    return JSONResponse(
        content = { 
            "message" : "Error occured during verification"
        },
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@user_router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    user = await user_service.get_user_by_email(email, db)
    if user:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email' : user.email,
                    "uid" : str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email' : user.email,
                    "uid" : str(user.uid)
                },
                refresh = True,
                expire=timedelta(days = Config.REFRESH_TOKEN_EXPIRES)
            )
            decoded_refresh_token = decode_access_token(refresh_token)

            # await add_jti_to_blocklist(decode_access_token['jti'])
            
            return JSONResponse(
                content={
                    'message' : "Login successful",
                    'access_token' : access_token,
                    "refresh_token" : refresh_token,
                    "user" : {
                        "email" : user.email,
                        "uid" : str(user.uid)
                    }
                }
            )
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Invalid Email or Password"
    )


@user_router.get("/logout")
async def revoke_token(token: str = Depends(oauth2_scheme)):
    
    payload = decode_access_token(token)
    jti = payload["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logged out successfully"}
    )

@user_router.get("/me")
async def get_current_user(user : UserBooksModel = Depends(get_current_user), _ : bool = Depends(role_checker)):
    return user


"""
1. Provide the email -> password reset request
2. Send password reset link
3. Reset password -> password reset confirm
"""

@user_router.post("/password-reset-request")
async def password_reset_request(email_data : PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({'email' : email})
    link = f"http://{Config.DOMAIN}:{Config.PORT}/api/v1/users/password-reset-confirm/{token}"
    
    html_message =f"""
    <h1>Reset your password</h1>
    <p>Please click this <a href='{link}'>link</a> to reset your password</p>
"""
    message = create_message(
        recipients=[email],
        subject = "Verify your email",
        body = html_message
    )
    
    await mail.send_message(message)

    return JSONResponse(
        content = {
            'message' : "Please check your email for instruction to reset your password"
        },
        status_code = status.HTTP_200_OK
    )

@user_router.post("/password-reset-confirm/{token}")
async def reset_account_password(token : str, passwords : PasswordResetConfirmModel,db : AsyncSession = Depends(get_db)):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password
    
    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match",
            status_code = status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(email=user_email, db=db)

        if not user:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="User not found"
            )
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {'password_hash' : password_hash}, db)
        

        return JSONResponse(
            content={
                "message" : "Password reset successfully"
            },
            status_code = status.HTTP_200_OK
        )
    return JSONResponse(
        content = { 
            "message" : "Error occured during password reset"
        },
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    )   




