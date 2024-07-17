from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_url: str = os.getenv("DATABASE_URL", "sqlite:///test.db")

engine = create_engine(database_url)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
