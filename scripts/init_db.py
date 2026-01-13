from sqlalchemy.ext.asyncio import create_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.config import settings
import asyncio


async def init_db():
    engine = create_engine(
        settings.DATABASE_URL.replace("+aiosqlite", ""),
        echo=settings.DEBUG
    )
    
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
