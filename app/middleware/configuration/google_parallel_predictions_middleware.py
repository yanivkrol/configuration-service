from app.frontend.confiugration.google_parallel_predictions_frontend import GoogleParallelPredictionsSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration.google_parallel_predictions import GoogleParallelPredictions


class GoogleParallelPredictionsMiddleware(BaseConfigurationMiddleware[GoogleParallelPredictionsSelection, GoogleParallelPredictions]):
    def to_database_object(self, selection: GoogleParallelPredictionsSelection) -> GoogleParallelPredictions:
        return GoogleParallelPredictions(
            account_id=selection.account.account_id,
            partner_id=selection.partner.partner_id,
            deal_type=selection.deal_type,
            active=selection.active,
        )
