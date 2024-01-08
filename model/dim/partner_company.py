from sqlalchemy import Column, String, BigInteger

from model import Base


class PartnerCompany(Base):
    __tablename__ = 'dim_partner_company'

    partner_id = Column(BigInteger, primary_key=True)
    company = Column(String, primary_key=True)
