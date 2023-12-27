from model.configuration.google_external_product import GoogleExternalProduct
from . import Response


class GoogleExternalProductResponse(Response[GoogleExternalProduct]):
    def get_key(self, record: GoogleExternalProduct) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'account_id': record.account_id,
            'campaign_id': record.campaign_id,
        }
