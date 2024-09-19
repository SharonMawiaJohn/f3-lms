from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def setup_db():
    engine = create_engine('sqlite:///learning_platform.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
