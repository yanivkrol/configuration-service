import sys

from configurations import ConfigurationId
from model.configuration.impl.google_external_product import GoogleExternalProduct
from model.configuration.impl.google_siteclick_postback import GoogleSiteclickPostback
from repository.base_repository import BaseRepository


class ConfigurationRepository(BaseRepository):
    pass


_google_external_product_repository = ConfigurationRepository(GoogleExternalProduct)
_google_siteclick_postback_repository = ConfigurationRepository(GoogleSiteclickPostback)


def get_repository(config_id: ConfigurationId) -> ConfigurationRepository:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_repository')
