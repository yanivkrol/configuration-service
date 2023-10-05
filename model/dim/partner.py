from sqlalchemy import Column, String, BigInteger

from model.serializable_model import SerializableModel


class Partner(SerializableModel):
    __tablename__ = 'dim_partner'

    partner_id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False) #, collation='utf8mb4_unicode_ci')
