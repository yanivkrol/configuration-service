from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_external_product_frontend import GoogleExternalProductSelection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.configuration.google_external_product import GoogleExternalProduct
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


class GoogleExternalProductMiddleware(BaseConfigurationMiddleware[GoogleExternalProductSelection, GoogleExternalProduct]):
    def get_model_type(self) -> type[GoogleExternalProduct]:
        return GoogleExternalProduct

    def to_database_object(self, selection: GoogleExternalProductSelection) -> GoogleExternalProduct:
        return GoogleExternalProduct(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )

    def _to_display_dict(self, selection: GoogleExternalProductSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'campaign_name': selection.campaign_mapping.campaign_name if selection.campaign_mapping else '__ALL__',
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleExternalProduct, GoogleAccount.account_name, GoogleAccountCampaignMappings.campaign_name) \
            .join(GoogleAccount, and_(
                GoogleExternalProduct.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],
            )) \
            .outerjoin(GoogleAccountCampaignMappings,
                GoogleExternalProduct.campaign_id == GoogleAccountCampaignMappings.campaign_id
            )
