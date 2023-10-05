from sqlalchemy import Column, String

from model.serializable_model import SerializableModel


class GoogleAccount(SerializableModel):
    __tablename__ = 'dim_google_account'

    mcc_id = Column(String(50), nullable=False)
    mcc_name = Column(String(250), nullable=False)
    account_id = Column(String(20), primary_key=True, nullable=False)
    account_name = Column(String(250), nullable=False)
