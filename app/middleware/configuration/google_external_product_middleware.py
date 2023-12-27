from app.frontend.confiugration.google_external_product_frontend import GoogleExternalProductSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.configuration.google_external_product import GoogleExternalProduct


class GoogleExternalProductMiddleware(BaseConfigurationMiddleware[GoogleExternalProductSelection, GoogleExternalProduct]):
    def to_database_object(self, selection: GoogleExternalProductSelection) -> GoogleExternalProduct:
        return GoogleExternalProduct(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )
