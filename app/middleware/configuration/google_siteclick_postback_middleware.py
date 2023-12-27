from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_siteclick_postback_frontend import GoogleSiteclickPostbackSelection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.configuration.google_siteclick_postback import GoogleSiteclickPostback
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


class GoogleSiteclickPostbackMiddleware(BaseConfigurationMiddleware[GoogleSiteclickPostbackSelection, GoogleSiteclickPostback]):
    def get_model_type(self) -> type[GoogleSiteclickPostback]:
        return GoogleSiteclickPostback

    def to_database_object(self, selection: GoogleSiteclickPostbackSelection) -> GoogleSiteclickPostback:
        return GoogleSiteclickPostback(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )

    def _to_display_dict(self, selection: GoogleSiteclickPostbackSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'campaign_name': selection.campaign_mapping.campaign_name if selection.campaign_mapping else '__ALL__',
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleSiteclickPostback, GoogleAccount.account_name, GoogleAccountCampaignMappings.campaign_name) \
            .join(GoogleAccount, and_(
                GoogleSiteclickPostback.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],
            )) \
            .outerjoin(GoogleAccountCampaignMappings,
                GoogleSiteclickPostback.campaign_id == GoogleAccountCampaignMappings.campaign_id
            )
