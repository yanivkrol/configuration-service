import sys
from typing import Protocol

from typing_extensions import Any

from configurations import ConfigurationId


class Response(Protocol):
    def get_key(self, record: Any) -> dict:
        ...

    def get_data(self, record: Any) -> dict | None:
        ...


from api.response.google_external_product_response import GoogleExternalProductResponse
from api.response.google_parallel_predictions_response import GoogleParallelPredictionsResponse
from api.response.google_postback_with_commission_response import GooglePostbackWithCommissionResponse
from api.response.google_siteclick_postback_response import GoogleSiteclickPostbackResponse

_google_external_product_response = GoogleExternalProductResponse()
_google_parallel_predictions_response = GoogleParallelPredictionsResponse()
_google_postback_with_commission_response = GooglePostbackWithCommissionResponse()
_google_siteclick_postback_response = GoogleSiteclickPostbackResponse()


def get_response(config_id: ConfigurationId) -> Response:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_response')
