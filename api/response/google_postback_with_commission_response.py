from model.configuration.google_postback_with_commission import GooglePostbackWithCommission
from . import Response


class GooglePostbackWithCommissionResponse(Response[GooglePostbackWithCommission]):
    def get_key(self, record: GooglePostbackWithCommission) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'account_id': record.account_id,
            'campaign_id': record.campaign_id,
        }
