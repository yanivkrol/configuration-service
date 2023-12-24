from collections import defaultdict
from dataclasses import dataclass

import pandas as pd

from app.frontend.components.column_display_functions import allable_campaign_column
from app.frontend.components.filters import AllableCampaignFilter
from app.frontend.components.new_sections import account_and_allable_campaign_selection
from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


@dataclass
class GooglePostbackWithCommissionSelection(Selection):
    account: GoogleAccount
    campaign_mapping: GoogleAccountCampaignMappings
    active: bool


class GooglePostbackWithCommissionFrontend(BaseConfigurationFrontend[GooglePostbackWithCommissionSelection]):

    def __init__(self):
        super().__init__(
            label="Google - Postback with Commission",
            display_name_mapping={
                "account_name": "Account name",
                "campaign_name": "Campaign name",
            },
            custom_column_filters={
                "campaign_name": AllableCampaignFilter(),
            },
            custom_column_display_function={
                "campaign_name": allable_campaign_column
            }
        )

    def render_new_section(self) -> GooglePostbackWithCommissionSelection | None:
        selected_account, all_campaigns_checked, selected_campaign = account_and_allable_campaign_selection()

        if all([selected_account, all_campaigns_checked or selected_campaign]):
            return GooglePostbackWithCommissionSelection(
                account=selected_account,
                campaign_mapping=None if all_campaigns_checked else selected_campaign,
                active=True,
            )
        return None

    def create_df_from_selections(self, selections: list[GooglePostbackWithCommissionSelection]) -> pd.DataFrame:
        selections_flattened = defaultdict(list)
        for selection in selections:
            selection_flattened = {}
            if selection.campaign_mapping:
                selection_flattened.update(selection.campaign_mapping.as_dict())
            else:
                selection_flattened.update(GoogleAccountCampaignMappings().as_dict())
            selection_flattened.update(selection.account.as_dict())
            selection_flattened['active'] = selection.active
            for k, v in selection_flattened.items():
                selections_flattened[k].append(v)
        return pd.DataFrame(selections_flattened)