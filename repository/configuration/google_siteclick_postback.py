from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.state_management import get_state, State
from model.configuration.google_siteclick_postback import GoogleSiteclickPostback
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.configuration import ConfigurationRepository


class GoogleSiteclickPostbackRepository(ConfigurationRepository[GoogleSiteclickPostback]):
    def __init__(self, session: Session):
        super().__init__(GoogleSiteclickPostback, session)  # TODO fix types

    def _get_as_df_query(self) -> Query:
        return self.session.query(GoogleSiteclickPostback, GoogleAccount, GoogleAccountCampaignMappings) \
            .join(GoogleAccount, and_(
                GoogleSiteclickPostback.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_name == get_state(State.COMPANY)['full'],  # TODO how not to use streamlit
            )) \
            .outerjoin(GoogleAccountCampaignMappings,GoogleSiteclickPostback.campaign_id == GoogleAccountCampaignMappings.campaign_id)
