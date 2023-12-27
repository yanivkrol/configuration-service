from sqlalchemy import Column, String, BigInteger

from model.serializable_model import SerializableModel


class PartnerCompany(SerializableModel):
    __tablename__ = 'dim_partner_company'

    partner_id = Column(BigInteger, primary_key=True)
    company = Column(String, primary_key=True)
