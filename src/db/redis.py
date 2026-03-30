from redis.asyncio import Redis
JTI_EXPIRY = 3600
from src.config import Config

token_blocklist = Redis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti : str) :
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti : str) -> bool:
    jti_bool = await token_blocklist.get(jti)

    return jti_bool is not None

