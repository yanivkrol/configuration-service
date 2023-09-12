from sqlalchemy import Integer, String, Column, Boolean, UniqueConstraint

from model.configuration.base_configuration import BaseConfiguration


class GoogleExternalProduct(BaseConfiguration):
    __tablename__ = 'configuration_google_external_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    external_partner_product_naming_enabled = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint('account_id', 'campaign_id', name='account_id__campaign_id'),
    )
