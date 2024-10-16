from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv('.env')
DATABASE_URL = os.getenv('DATABASE_URL')
#  Define the database URL (adjust it for your database)
#DATABASE_URL = "postgresql://postgres:postgres21@localhost/image_storage"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for your models
Base = declarative_base()

# Dependency function to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
