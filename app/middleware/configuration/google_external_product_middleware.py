from app.frontend.confiugration.google_external_product_frontend import GoogleExternalProductSelection
from app.middleware.configuration.account_campaign_middleware import AccountCampaignMiddleware
from model.configuration.google_external_product import GoogleExternalProduct


class GoogleExternalProductMiddleware(AccountCampaignMiddleware[GoogleExternalProductSelection, GoogleExternalProduct]):
    def __init__(self):
        super().__init__(source_join='google')

    def get_model_type(self) -> type[GoogleExternalProduct]:
        return GoogleExternalProduct
