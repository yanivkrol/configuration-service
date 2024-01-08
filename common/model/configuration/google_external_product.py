from sqlalchemy import Integer, String, Column, Boolean

from common.model import Base


class GoogleExternalProduct(Base):
    __tablename__ = 'configuration_google_external_product'

    id = Column(Integer, primary_key=True)
    mcc_id = Column(String)
    account_id = Column(String)
    campaign_id = Column(String)
    active = Column(Boolean)
