from typing import Literal, get_args


ConfigurationId = Literal[
    "google_external_product",
    "google_parallel_predictions",
    "google_postback_with_commission",
    "google_siteclick_postback",
]


def get_all_configurations() -> tuple[str]:
    return get_args(ConfigurationId)
