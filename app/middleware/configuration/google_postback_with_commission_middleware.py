from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_postback_with_commission_frontend import GooglePostbackWithCommissionSelection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.configuration.google_postback_with_commission import GooglePostbackWithCommission
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


class GooglePostbackWithCommissionMiddleware(BaseConfigurationMiddleware[GooglePostbackWithCommissionSelection, GooglePostbackWithCommission]):
    def get_model_type(self) -> type[GooglePostbackWithCommission]:
        return GooglePostbackWithCommission

    def to_database_object(self, selection: GooglePostbackWithCommissionSelection) -> GooglePostbackWithCommission:
        return GooglePostbackWithCommission(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )

    def _to_display_dict(self, selection: GooglePostbackWithCommissionSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'campaign_name': selection.campaign_mapping.campaign_name if selection.campaign_mapping else '__ALL__',
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GooglePostbackWithCommission, GoogleAccount.account_name, GoogleAccountCampaignMappings.campaign_name) \
            .join(GoogleAccount, and_(
                GooglePostbackWithCommission.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],
            )) \
            .outerjoin(GoogleAccountCampaignMappings,
                GooglePostbackWithCommission.campaign_id == GoogleAccountCampaignMappings.campaign_id
            )
