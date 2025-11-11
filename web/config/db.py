import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import config
import asyncio
from sqlalchemy.orm import sessionmaker

url = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"

engine = create_async_engine(
    url,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=0
)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
