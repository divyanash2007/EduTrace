from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core import config

DB_URL = config.DB_URL

engine = create_engine(DB_URL,echo=False,future=True)
sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()