import enum

from sqlalchemy import Integer, String, Column, Boolean, Enum

from model.serializable_model import SerializableModel


class DealType(str, enum.Enum):  # str for JSON serialization
    LEAD = "Lead"
    SALE = "Sale"
    REV_SHARE = "Rev Share"
    FTD = "FTD"
    SUBSCRIBER = "Subscriber"
    SIGN_UP = "Sign Up"
    REGISTRATION = "Registration"
    QUALIFIED_LEAD = "Qualified Lead"
    INSTALL = "Install"
    OTHER = "Other"
    CLICK = "Click"
    MULTI = "Multi"
    NONE = "None"


class GoogleParallelPredictions(SerializableModel):
    __tablename__ = 'configuration_google_parallel_predictions'

    id = Column(Integer, primary_key=True)
    account_id = Column(String)
    partner_id = Column(String)
    deal_type = Column(Enum(DealType))
    active = Column(Boolean)
