from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

DATABASE_URL = settings.DATABASE_URL
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_size": 8,
    "max_overflow": 4,
    "pool_timeout": 10,
    "pool_recycle": 300,
}


database = Database(DATABASE_URL)
db_url = DATABASE_URL
dynamic_engine = create_engine(db_url, **SQLALCHEMY_ENGINE_OPTIONS)
dynamic_session = sessionmaker(autocommit=False, autoflush=False, bind=dynamic_engine)
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
