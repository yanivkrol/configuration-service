from sqlalchemy import Integer, String, Column, Boolean, UniqueConstraint

from model.serializable_model import SerializableModel


class GoogleSiteclickPostback(SerializableModel):
    __tablename__ = 'configuration_google_siteclick_postback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    external_partner_product_naming_enabled = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint('account_id', 'campaign_id', name='account_id__campaign_id'),
    )
