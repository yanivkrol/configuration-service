import sys

from app.configuration_frontend.base_configuration_frontend import BaseConfigurationFrontend
from configurations import ConfigurationId
from .impl.google_external_product_frontend import GoogleExternalProductFrontend
from .impl.google_siteclick_postback_frontend import GoogleSiteclickPostbackFrontend


_google_external_product_frontend = GoogleExternalProductFrontend()
_google_siteclick_postback_frontend = GoogleSiteclickPostbackFrontend()


def get_frontend(config_id: ConfigurationId) -> BaseConfigurationFrontend:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_frontend')
