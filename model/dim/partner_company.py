from sqlalchemy import Column, String, BigInteger

from model.serializable_model import SerializableModel


class PartnerCompany(SerializableModel):
    __tablename__ = 'dim_partner_company'

    partner_id = Column(BigInteger, primary_key=True, nullable=False)
    company = Column(String(20), primary_key=True, nullable=False)
