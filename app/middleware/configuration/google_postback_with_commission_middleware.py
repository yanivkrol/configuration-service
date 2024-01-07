from app.frontend.confiugration.google_postback_with_commission_frontend import GooglePostbackWithCommissionSelection
from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from model.configuration.google_postback_with_commission import GooglePostbackWithCommission


class GooglePostbackWithCommissionMiddleware(AccountCampaignMiddleware[GooglePostbackWithCommissionSelection, GooglePostbackWithCommission]):
    def __init__(self):
        super().__init__(source_join='google')

    def get_model_type(self) -> type[GooglePostbackWithCommission]:
        return GooglePostbackWithCommission
