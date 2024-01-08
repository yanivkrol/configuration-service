from common.model.configuration import GoogleActivePostback
from . import Response


class GoogleActivePostbackResponse(Response[GoogleActivePostback]):
    def get_key(self, record: GoogleActivePostback) -> dict:
        return {
            'account_id': record.account_id,
            'site_id': record.site_id,
            'vertical_id': record.vertical_id,
            'traffic_join': record.traffic_join.name,
        }

    def get_data(self, record: GoogleActivePostback) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'mcc_name': record.mcc_name,
        }
