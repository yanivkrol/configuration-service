from sqlalchemy import Column, String, BigInteger

from model import Base


class SiteVerticalMapping(Base):
    __tablename__ = 'dim_site_vertical_mapping'

    site_id = Column(BigInteger, primary_key=True)
    vertical_id = Column(String, primary_key=True)
