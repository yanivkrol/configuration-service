from sqlalchemy import Integer, String, Column, Boolean

from model import Base


class GoogleSiteclickPostback(Base):
    __tablename__ = 'configuration_google_siteclick_postback'

    id = Column(Integer, primary_key=True)
    mcc_id = Column(String)
    account_id = Column(String)
    campaign_id = Column(String)
    active = Column(Boolean)
