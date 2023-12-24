from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.state_management import get_state, State
from model.configuration.google_postback_with_commission import GooglePostbackWithCommission
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.configuration import ConfigurationRepository


class GooglePostbackWithCommissionRepository(ConfigurationRepository[GooglePostbackWithCommission]):
    def __init__(self, session: Session):
        super().__init__(GooglePostbackWithCommission, session)  # TODO fix types

    def _get_as_df_query(self, limit: Optional[int] = None) -> Query:
        return self.session.query(GooglePostbackWithCommission, GoogleAccount, GoogleAccountCampaignMappings) \
            .join(GoogleAccount, and_(
                GooglePostbackWithCommission.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_name == get_state(State.COMPANY)['full'],  # TODO how not to use streamlit
            )) \
            .outerjoin(GoogleAccountCampaignMappings,GooglePostbackWithCommission.campaign_id == GoogleAccountCampaignMappings.campaign_id)