from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.state_management import get_state, State
from model.configuration.google_external_product import GoogleExternalProduct
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.configuration import ConfigurationRepository


class GoogleExternalProductRepository(ConfigurationRepository[GoogleExternalProduct]):
    def __init__(self, session: Session):
        super().__init__(GoogleExternalProduct, session)  # TODO fix types

    def _get_as_df_query(self) -> Query:
        return self.session.query(GoogleExternalProduct, GoogleAccount, GoogleAccountCampaignMappings) \
            .join(GoogleAccount, and_(
                GoogleExternalProduct.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],  # TODO how not to use streamlit
            )) \
            .outerjoin(GoogleAccountCampaignMappings,
                GoogleExternalProduct.campaign_id == GoogleAccountCampaignMappings.campaign_id
           )
