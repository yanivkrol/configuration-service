from sqlalchemy import Integer, String, Column, Boolean

from model.serializable_model import SerializableModel


class GoogleExternalProduct(SerializableModel):
    __tablename__ = 'configuration_google_external_product'

    id = Column(Integer, primary_key=True)
    mcc_id = Column(String)
    account_id = Column(String)
    campaign_id = Column(String)
    active = Column(Boolean)
