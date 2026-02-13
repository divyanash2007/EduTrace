from typing import Generator
from app.core.database import sessionlocal

def get_db() -> Generator:
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
