import sys

from configurations import ConfigurationId
from db_config import db_session
from model.configuration.impl.google_external_product import GoogleExternalProduct
from .configuration_repository import ConfigurationRepository
from .impl.google_external_product import GoogleExternalProductRepository

_google_external_product_repository = GoogleExternalProductRepository(GoogleExternalProduct, db_session)
# _google_siteclick_postback_repository = ConfigurationRepository(GoogleSiteclickPostback, db_session)


def get_repository(config_id: ConfigurationId) -> ConfigurationRepository:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_repository')
