from sqlalchemy import Integer, String, Column, UniqueConstraint, Boolean

from model.serializable_model import SerializableModel


class GoogleExternalProduct(SerializableModel):
    __tablename__ = 'configuration_google_external_product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint('account_id', 'campaign_id', name='account_id__campaign_id'),
    )
