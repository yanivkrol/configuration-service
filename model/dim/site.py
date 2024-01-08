from sqlalchemy import Column, String, BigInteger

from model import Base


class Site(Base):
    __tablename__ = 'dim_site'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
