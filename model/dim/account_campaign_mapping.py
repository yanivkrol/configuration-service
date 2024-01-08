from sqlalchemy import Column, String

from model import Base


class AccountCampaignMapping(Base):
    __tablename__ = 'dim_account_campaign_mappings'

    source_join = Column(String, primary_key=True)
    account_id = Column(String, primary_key=True)
    account_name = Column(String)
    campaign_id = Column(String, primary_key=True)
    campaign_name = Column(String)
