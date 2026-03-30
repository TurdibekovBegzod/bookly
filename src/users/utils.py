from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
import jwt
from src.config import Config
import logging 
import uuid
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(
    secret_key=Config.SECRET_KEY,
    salt='email-configuration'
)

ACCESS_TOKEN_EXPIRES = 30

pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated = 'auto'
)

def generate_password_hash(password : str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
        user_data : dict, 
        expire : timedelta = timedelta(seconds=Config.ACCESS_TOKEN_EXPIRES), refresh : bool = False
):
    payload = {}
    payload["sub"] = str(user_data["uid"])
    payload['user']  = user_data
    payload['exp'] = datetime.now(timezone.utc) + (
        expire if expire else timedelta(seconds=Config.ACCESS_TOKEN_EXPIRES)
    )
    payload['refresh'] = refresh
    payload['jti'] = str(uuid.uuid4())


    token = jwt.encode(
        payload=payload,
        key=Config.SECRET_KEY,
        algorithm=Config.ALGORITHM
    )

    return token

def decode_access_token(token : str) -> dict:
    try:
        token_data = jwt.decode(
            jwt = token,
            key=Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM],
            
        )
        return token_data
    
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    
def create_url_safe_token(data : dict):
    token = serializer.dumps(
        data, salt="email-configuration"
    )
    return token


def decode_url_safe_token(token : str):
    try:
        token_data : dict = serializer.loads(token, salt="email-configuration")
        return token_data

    except Exception as e:
        logging.error(str(e))