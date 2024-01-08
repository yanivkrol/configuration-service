from sqlalchemy import Integer, String, Column, Boolean, Enum
from model import Base

from common.enums import DealType


class GoogleParallelPredictions(Base):
    __tablename__ = 'configuration_google_parallel_predictions'

    id = Column(Integer, primary_key=True)
    account_id = Column(String)
    partner_id = Column(String)
    deal_type = Column(Enum(DealType))
    active = Column(Boolean)
