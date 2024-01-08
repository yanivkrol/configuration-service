from sqlalchemy import Column, String, BigInteger

from common.model import Base


class Partner(Base):
    __tablename__ = 'dim_partner'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
