from model.configuration.google_siteclick_postback import GoogleSiteclickPostback
from . import Response


class GoogleSiteclickPostbackResponse(Response[GoogleSiteclickPostback]):
    def get_key(self, record: GoogleSiteclickPostback) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'account_id': record.account_id,
            'campaign_id': record.campaign_id,
        }
