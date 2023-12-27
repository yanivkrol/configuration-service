from sqlalchemy import Integer, String, Column, Boolean

from model.serializable_model import SerializableModel


class GooglePostbackWithCommission(SerializableModel):
    __tablename__ = 'configuration_google_postback_with_commission'

    id = Column(Integer, primary_key=True)
    mcc_id = Column(String)
    account_id = Column(String)
    campaign_id = Column(String)
    active = Column(Boolean)
