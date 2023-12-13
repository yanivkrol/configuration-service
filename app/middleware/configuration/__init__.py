import sys
from typing import TypeVar, Protocol

from configurations import ConfigurationId
from app.frontend.confiugration import Selection
from model.serializable_model import SerializableModel

S = TypeVar('S', bound=Selection)
T = TypeVar('T', bound=SerializableModel)


class BaseConfigurationMiddleware(Protocol[S, T]):
    def to_database_object(self, selection: S) -> T:
        ...


from app.middleware.configuration.google_external_product_middleware import GoogleExternalProductMiddleware
from app.middleware.configuration.google_siteclick_postback_middleware import GoogleSiteclickPostbackMiddleware
from app.middleware.configuration.google_parallel_predictions_middleware import GoogleParallelPredictionsMiddleware
from app.middleware.configuration.google_postback_with_commission_middleware import GooglePostbackWithCommissionMiddleware

_google_external_product_middleware = GoogleExternalProductMiddleware()
_google_siteclick_postback_middleware = GoogleSiteclickPostbackMiddleware()
_google_parallel_predictions_middleware = GoogleParallelPredictionsMiddleware()
_google_postback_with_commission_middleware = GooglePostbackWithCommissionMiddleware()


def get_middleware(config_id: ConfigurationId) -> BaseConfigurationMiddleware:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_middleware')



