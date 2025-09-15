from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator, Any

# psycopg3 async driver
DATABASE_URL = "postgresql+psycopg://postgres:2425@localhost:5432/postgres"

# Create async engine (SQLAlchemy manages psycopg3 pool internally)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    # pool_size=5,        # min pool size
    pool_size=50,        # min pool size
    # max_overflow=10,    # extra connections allowed
    max_overflow=100,    # extra connections allowed
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency for FastAPI
async def get_db() -> AsyncGenerator[Any, Any]:
    async with AsyncSessionLocal() as session:
        yield session
