from sqlalchemy import Integer, String, Column, Boolean, Enum

from common.enums import TrafficJoin
from common.model import Base


class GoogleActivePostback(Base):
    __tablename__ = 'configuration_google_active_postback'

    id = Column(Integer, primary_key=True)
    mcc_id = Column(String)
    mcc_name = Column(String)
    site_id = Column(Integer)
    vertical_id = Column(String)
    traffic_join = Column(Enum(TrafficJoin))
    account_id = Column(String)
    active = Column(Boolean)
