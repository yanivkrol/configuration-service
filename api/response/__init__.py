import sys
from typing import Protocol, TypeVar

from sqlalchemy.orm import DeclarativeBase

from configurations import ConfigurationId

T = TypeVar('T', bound=DeclarativeBase)


class Response(Protocol[T]):
    def get_key(self, record: T) -> dict:
        ...

    def get_data(self, record: T) -> dict | None:
        return None


from .google_external_product_response import GoogleExternalProductResponse
from .google_parallel_predictions_response import GoogleParallelPredictionsResponse
from .google_postback_with_commission_response import GooglePostbackWithCommissionResponse
from .google_siteclick_postback_response import GoogleSiteclickPostbackResponse

_google_external_product_response = GoogleExternalProductResponse()
_google_parallel_predictions_response = GoogleParallelPredictionsResponse()
_google_postback_with_commission_response = GooglePostbackWithCommissionResponse()
_google_siteclick_postback_response = GoogleSiteclickPostbackResponse()


def get_response(config_id: ConfigurationId) -> Response:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_response')
