from app.frontend.confiugration.google_siteclick_postback_frontend import GoogleSiteclickPostbackSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration.google_siteclick_postback import GoogleSiteclickPostback


class GoogleSiteclickPostbackMiddleware(BaseConfigurationMiddleware[GoogleSiteclickPostbackSelection, GoogleSiteclickPostback]):
    def to_database_object(self, selection: GoogleSiteclickPostbackSelection) -> GoogleSiteclickPostback:
        return GoogleSiteclickPostback(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=selection.campaign_mapping.campaign_id if selection.campaign_mapping else "__ALL__",
            rollout_type=selection.rollout_type,
            active=selection.active,
        )
