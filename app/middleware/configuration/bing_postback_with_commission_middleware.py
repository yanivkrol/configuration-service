from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from model.configuration.bing_postback_with_commission import BingPostbackWithCommission


class BingPostbackWithCommissionMiddleware(AccountCampaignMiddleware[BingPostbackWithCommission]):
    def __init__(self):
        super().__init__(source_join='bing')

    def get_model_type(self) -> type[BingPostbackWithCommission]:
        return BingPostbackWithCommission
