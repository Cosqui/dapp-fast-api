from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHAMY_DATABASe_URL = 'sqlite:///./icommerce.db'

engine = create_engine(SQLALCHAMY_DATABASe_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False)

Base = declarative_base()