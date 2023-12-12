from dataclasses import dataclass

import pandas as pd

from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection


@dataclass
class GoogleSiteclickPostbackSelection(Selection):
    pass


class GoogleSiteclickPostbackFrontend(BaseConfigurationFrontend[GoogleSiteclickPostbackSelection]):

    def __init__(self):
        super().__init__(
            label="Google - Siteclick Postback",
            display_name_mapping={
                "mcc_id": "MCC ID",
                "account_id": "Account ID",
                "campaign_id": "Campaign ID",
            }
        )

    def render_new_section(self) -> GoogleSiteclickPostbackSelection | None:  # TODO
        pass

    def create_df_from_selections(self, selections: list[GoogleSiteclickPostbackSelection]) -> pd.DataFrame:
        pass
