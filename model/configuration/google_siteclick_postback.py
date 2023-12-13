import enum

from sqlalchemy import Integer, String, Column, UniqueConstraint, Boolean, Enum

from model.serializable_model import SerializableModel


class RolloutType(enum.Enum):
    TO_SEND = "To Send"


class GoogleSiteclickPostback(SerializableModel):
    __tablename__ = 'configuration_google_siteclick_postback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mcc_id = Column(String, nullable=False)
    account_id = Column(String, nullable=False)
    campaign_id = Column(String, nullable=False)
    rollout_type = Column(Enum(RolloutType), nullable=False)
    active = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint('account_id', 'campaign_id', name='account_id__campaign_id'),
    )
