from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.configs import settings
from . import settings
import logging

DATABASE_URL = settings.DATABASE_URL_POSTGRES
logging.info(DATABASE_URL)
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_size": 2,
    "max_overflow": 4,
    "pool_timeout": 10,
    "pool_recycle": 300,
}


database = Database(DATABASE_URL)
db_url = DATABASE_URL
dynamic_engine = create_engine(db_url, ** SQLALCHEMY_ENGINE_OPTIONS)
dynamic_session = sessionmaker(
    autocommit=False, autoflush=False, bind=dynamic_engine)
Base = declarative_base(metadata=MetaData(bind=dynamic_engine))
metadata = Base.metadata


def get_db():
    db = dynamic_session()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()


async def on_start():
    # await database.connect()
    metadata.create_all(dynamic_engine)
    logging.info("connect success")


async def on_shutdown():
    await database.disconnect()
