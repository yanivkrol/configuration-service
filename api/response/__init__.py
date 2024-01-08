import sys
from typing import Protocol, TypeVar

from common.configurations import ConfigurationId
from common.model import Base

T = TypeVar('T', bound=Base)


class Response(Protocol[T]):
    def get_key(self, record: T) -> dict:
        ...

    def get_data(self, record: T) -> dict | None:
        return None


from .account_campaign_response import AccountCampaignResponse
from .google_active_postback_response import GoogleActivePostbackResponse
from .google_parallel_predictions_response import GoogleParallelPredictionsResponse

_bing_postback_with_commission_response = AccountCampaignResponse()
_google_active_postback_response = GoogleActivePostbackResponse()
_google_external_product_response = AccountCampaignResponse()
_google_parallel_predictions_response = GoogleParallelPredictionsResponse()
_google_postback_with_commission_response = AccountCampaignResponse()
_google_siteclick_postback_response = AccountCampaignResponse()


def get_response(config_id: ConfigurationId) -> Response:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_response')
