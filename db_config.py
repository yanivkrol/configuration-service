from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql://root:root@127.0.0.1:3306/configuration_service"  # TODO env var

engine = create_engine(DATABASE_URL)
SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()
