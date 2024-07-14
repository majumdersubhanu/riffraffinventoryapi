from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///test.db"))

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
