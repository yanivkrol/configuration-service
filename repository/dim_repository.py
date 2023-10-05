from typing import TypeVar, Type

from sqlalchemy.orm import Session

from db_config import db_session
from model.dim.base_dim import BaseDim
from model.dim.impl.google_account import GoogleAccount
from model.dim.impl.google_account_campaigns_mapping import GoogleAccountCampaignMappings
from model.dim.impl.partner import Partner
from model.dim.impl.partner_company import PartnerCompany
from repository.base_repository import BaseRepository

DimModelT = TypeVar('DimModelT', bound=BaseDim)


class DimRepository(BaseRepository):
    def __init__(self, model: Type[DimModelT], session: Session):
        super().__init__(model, session)


dim_google_account_repository = DimRepository(GoogleAccount, db_session)
dim_google_account_campaigns_mapping_repository = DimRepository(GoogleAccountCampaignMappings, db_session)
dim_partner_repository = DimRepository(Partner, db_session)
dim_partner_company_repository = DimRepository(PartnerCompany, db_session)
