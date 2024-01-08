from model.configuration.google_parallel_predictions import GoogleParallelPredictions
from . import Response


class GoogleParallelPredictionsResponse(Response[GoogleParallelPredictions]):
    def get_key(self, record: GoogleParallelPredictions) -> dict:
        return {
            'account_id': record.account_id,
            'partner_id': record.partner_id,
            'deal_type': record.deal_type.name,
        }
