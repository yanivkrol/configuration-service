from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from common.model.configuration.google_siteclick_postback import GoogleSiteclickPostback


class GoogleSiteclickPostbackMiddleware(AccountCampaignMiddleware[GoogleSiteclickPostback]):
    def __init__(self):
        super().__init__(source_join='google')

    def get_model_type(self) -> type[GoogleSiteclickPostback]:
        return GoogleSiteclickPostback
