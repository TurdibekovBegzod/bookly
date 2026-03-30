from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import Config
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

DBSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        print("Creating database tables...")
        print(Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        await db.close() 