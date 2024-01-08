from sqlalchemy import Column, String

from model import Base


class Vertical(Base):
    __tablename__ = 'dim_vertical'

    id = Column(String, primary_key=True)
    name = Column(String)
