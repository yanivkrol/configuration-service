from sqlalchemy import Column, String

from model.serializable_model import SerializableModel


class Account(SerializableModel):
    __tablename__ = 'dim_account'

    source_join = Column(String)
    mcc_id = Column(String)
    mcc_name = Column(String)
    account_id = Column(String, primary_key=True)
    account_name = Column(String)
