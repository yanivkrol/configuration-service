from typing_extensions import Any

from . import Response


class GooglePostbackWithCommissionResponse(Response):
    def get_key(self, record: Any) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'account_id': record.account_id,
            'campaign_id': record.campaign_id,
        }

    def get_data(self, record: Any) -> dict | None:
        return None
