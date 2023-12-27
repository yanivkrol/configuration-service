from sqlalchemy import Column, String, BigInteger

from model.serializable_model import SerializableModel


class Partner(SerializableModel):
    __tablename__ = 'dim_partner'

    partner_id = Column(BigInteger, primary_key=True)
    name = Column(String)
