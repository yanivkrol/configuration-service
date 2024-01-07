from sqlalchemy import Column, String

from model.serializable_model import SerializableModel


class AccountCampaignMapping(SerializableModel):
    __tablename__ = 'dim_account_campaign_mappings'

    source_join = Column(String, primary_key=True)
    account_id = Column(String, primary_key=True)
    account_name = Column(String)
    campaign_id = Column(String, primary_key=True)
    campaign_name = Column(String)
