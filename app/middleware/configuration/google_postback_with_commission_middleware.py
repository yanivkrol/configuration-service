from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from common.model.configuration import GooglePostbackWithCommission


class GooglePostbackWithCommissionMiddleware(AccountCampaignMiddleware[GooglePostbackWithCommission]):
    def __init__(self):
        super().__init__(source_join='google')

    def get_model_type(self) -> type[GooglePostbackWithCommission]:
        return GooglePostbackWithCommission
