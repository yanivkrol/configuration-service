from app.frontend.confiugration.google_siteclick_postback_frontend import GoogleSiteclickPostbackSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.configuration.google_siteclick_postback import GoogleSiteclickPostback


class GoogleSiteclickPostbackMiddleware(BaseConfigurationMiddleware[GoogleSiteclickPostbackSelection, GoogleSiteclickPostback]):
    def to_database_object(self, selection: GoogleSiteclickPostbackSelection) -> GoogleSiteclickPostback:
        return GoogleSiteclickPostback(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )
