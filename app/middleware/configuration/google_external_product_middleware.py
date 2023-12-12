from app.frontend.confiugration.google_external_product_frontend import GoogleExternalProductSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration.google_external_product import GoogleExternalProduct


class GoogleExternalProductMiddleware(BaseConfigurationMiddleware[GoogleExternalProductSelection, GoogleExternalProduct]):
    def to_database_object(self, selection: GoogleExternalProductSelection) -> GoogleExternalProduct:
        return GoogleExternalProduct(
            account_id=selection.account.account_id,
            campaign_id=selection.campaign_mapping.campaign_id if selection.campaign_mapping else "__ALL__",
            active=selection.active,
        )
