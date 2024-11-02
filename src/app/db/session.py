from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Create the asynchronous engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True,
    future=True,
)

# Create the asynchronous sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
