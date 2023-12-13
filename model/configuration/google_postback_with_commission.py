from sqlalchemy import Integer, String, Column, UniqueConstraint, Boolean, DateTime

from model.serializable_model import SerializableModel


class GooglePostbackWithCommission(SerializableModel):
    __tablename__ = 'configuration_google_postback_with_commission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mcc_id = Column(String, nullable=False)
    account_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime)
    active = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint('account_id', 'campaign_id', name='account_id__campaign_id'),
    )
