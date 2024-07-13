from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///test.db")

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
