from typing_extensions import Any

from . import Response


class GoogleParallelPredictionsResponse(Response):
    def get_key(self, record: Any) -> dict:
        return {
            'account_id': record.account_id,
            'partner_id': record.partner_id,
            'deal_type': record.deal_type,
        }

    def get_data(self, record: Any) -> dict | None:
        return None
