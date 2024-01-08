from enum import Enum


class SerializableEnum(str, Enum):
    pass


class DealType(SerializableEnum):  # str for JSON serialization
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


class TrafficJoin(SerializableEnum):  # str for JSON serialization
    VIDEO = "Video"
    EMAIL = "Email"
    DISPLAY = "Display"
    PAID_SEARCH = "Paid Search"
    ORGANIC_SEARCH = "Organic Search"
    PAID_SOCIAL = "Paid Social"
    ORGANIC_SOCIAL = "Organic Social"
    NATIVE = "Native"
    AFFILIATES = "Affiliates"
    OTHER = "Other"
    DIRECT = "Direct"
    DV360 = "DV360"
    MOBILE_APPS = "Mobile Apps"
    PUBLISHERS = "Publishers"
    PMAX = "PerformanceMax"
    DISCOVERY = "Discovery"
    WHATSAPP = "WhatsApp"
    SMS = "SMS"