from dataclasses import dataclass

from app.frontend.components.column_display_functions import allable_campaign_column
from app.frontend.components.filters import AllableCampaignFilter
from app.frontend.components.new_sections import account_and_allable_campaign_selection
from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


@dataclass
class GoogleExternalProductSelection(Selection):
    account: GoogleAccount
    campaign_mapping: GoogleAccountCampaignMappings
    active: bool


class GoogleExternalProductFrontend(BaseConfigurationFrontend[GoogleExternalProductSelection]):

    def __init__(self):
        super().__init__(
            label="Google - External Product",
            display_name_mapping={
                "account_name": "Account name",
                "campaign_name": "Campaign name",
            },
            custom_column_filters={
                "campaign_name": AllableCampaignFilter()
            },
            custom_column_display_function={
                "campaign_name": allable_campaign_column
            }
        )

    def render_new_section(self) -> GoogleExternalProductSelection | None:
        selected_account, selected_campaign = account_and_allable_campaign_selection()

        if all([selected_account, selected_campaign]):
            return GoogleExternalProductSelection(
                account=selected_account,
                campaign_mapping=None if selected_campaign == "__ALL__" else selected_campaign,
                active=True,
            )
        return None
