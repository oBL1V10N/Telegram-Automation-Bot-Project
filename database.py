from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# Example setup for AsyncSession
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Adjust this for your database

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create sessionmaker using AsyncSession
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# A function that returns an AsyncSession (this might be where you're encountering the error)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        # Yielding session to be used for database operations
        yield session
