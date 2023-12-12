from typing import TypeVar, Type

from sqlalchemy.orm import Session

from db_config import db_session
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from model.dim.partner import Partner
from model.dim.partner_company import PartnerCompany
from model.serializable_model import SerializableModel
from repository.base_repository import BaseRepository

DimModelT = TypeVar('DimModelT', bound=SerializableModel)


class DimRepository(BaseRepository[DimModelT]):
    def __init__(self, model: Type[DimModelT], session: Session):
        super().__init__(model, session)


dim_google_account_repository = DimRepository[GoogleAccount](GoogleAccount, db_session)
dim_google_account_campaigns_mapping_repository = DimRepository[GoogleAccountCampaignMappings](GoogleAccountCampaignMappings, db_session)
dim_partner_repository = DimRepository[Partner](Partner, db_session)
dim_partner_company_repository = DimRepository[PartnerCompany](PartnerCompany, db_session)
