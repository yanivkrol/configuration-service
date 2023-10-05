from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.configuration_frontend.google_external_product_frontend import GoogleExternalProductSelection
from app.state_management import get_state, State
from model.configuration.google_external_product import GoogleExternalProduct
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from model.serializable_model import SerializableModel
from repository.configuration.configuration_repository import ConfigurationRepository


class GoogleExternalProductRepository(ConfigurationRepository[GoogleExternalProduct, GoogleExternalProductSelection]):
    def __init__(self, session: Session):
        super().__init__(GoogleExternalProduct, session)  # TODO fix types

    def _get_as_df_query(self, limit: Optional[int] = None) -> Query:
        return self.session.query(GoogleExternalProduct, GoogleAccount, GoogleAccountCampaignMappings) \
            .join(GoogleAccount, and_(
                GoogleExternalProduct.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_name == get_state(State.COMPANY)['full'],  # TODO how not to use streamlit
            )) \
            .outerjoin(GoogleAccountCampaignMappings, GoogleExternalProduct.campaign_id == GoogleAccountCampaignMappings.campaign_id)

    def add_from_selections(self, selections: list[GoogleExternalProductSelection]):  # TODO better name, better API
        for selection in selections:
            configuration = GoogleExternalProduct(
                account_id=selection.account.account_id,
                campaign_id=selection.campaign_mapping.campaign_id if selection.campaign_mapping else None,
                active=selection.active,
            )
            self.add(configuration)
