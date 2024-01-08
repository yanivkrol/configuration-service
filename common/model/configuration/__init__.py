import sys
from typing import Type

from common.configurations import ConfigurationId
from common.model import Base
from .bing_postback_with_commission import BingPostbackWithCommission
from .google_active_postback import GoogleActivePostback
from .google_external_product import GoogleExternalProduct
from .google_parallel_predictions import GoogleParallelPredictions
from .google_postback_with_commission import GooglePostbackWithCommission
from .google_siteclick_postback import GoogleSiteclickPostback

_bing_postback_with_commission_model = BingPostbackWithCommission
_google_active_postback_model = GoogleActivePostback
_google_external_product_model = GoogleExternalProduct
_google_parallel_predictions_model = GoogleParallelPredictions
_google_postback_with_commission_model = GooglePostbackWithCommission
_google_siteclick_postback_model = GoogleSiteclickPostback


def get_model(config_id: ConfigurationId) -> Type[Base]:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_model')
