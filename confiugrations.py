from configuration.google.external_product import GoogleExternalProduct
from configuration.google.siteclick_postback import GoogleSiteclickPostback


google_sitelick_postback = GoogleSiteclickPostback()
google_external_product = GoogleExternalProduct()

all = [
    google_sitelick_postback,
    google_external_product
]

all_by_name = {config.name: config for config in all}
