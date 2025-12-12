import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

class DataBaseConfig:
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    def uri_postgres(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DATABASE_NAME}"
    
db_config = DataBaseConfig()

async_engine: AsyncEngine = create_async_engine(db_config.uri_postgres(), echo=True)
async_session = async_sessionmaker(bind=async_engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session as session:
        yield session