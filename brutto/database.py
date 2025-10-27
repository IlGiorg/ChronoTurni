from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./test.db')


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    import app.models as models
    Base.metadata.create_all(bind=engine)