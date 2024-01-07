from app.frontend.confiugration.google_siteclick_postback_frontend import GoogleSiteclickPostbackSelection
from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from model.configuration.google_siteclick_postback import GoogleSiteclickPostback


class GoogleSiteclickPostbackMiddleware(AccountCampaignMiddleware[GoogleSiteclickPostbackSelection, GoogleSiteclickPostback]):
    def __init__(self):
        super().__init__(source_join='google')

    def get_model_type(self) -> type[GoogleSiteclickPostback]:
        return GoogleSiteclickPostback
