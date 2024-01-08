from abc import ABC
from dataclasses import dataclass

import streamlit as st

from app.frontend.components.filters import AllableCampaignFilter
from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from app.frontend.state_management import get_state, State
from app.middleware.dim_service import dim_service
from model.dim.account import Account
from model.dim.account_campaign_mapping import AccountCampaignMapping


@dataclass
class AccountCampaignSelection(Selection):
    account: Account
    campaign_mapping: AccountCampaignMapping
    active: bool


class AccountCampaignFrontend(BaseConfigurationFrontend[AccountCampaignSelection], ABC):

    def __init__(self, label: str, source_join: str):
        super().__init__(
            label=label,
            display_name_mapping={
                "account_name": "Account name",
                "campaign_name": "Campaign name",
            },
            custom_column_filters={
                "campaign_name": AllableCampaignFilter(),
            },
            custom_column_display_function={
                "campaign_name": lambda series: series.apply(lambda c: c or "All campaigns")
            }
        )
        self._source_join = source_join

    def render_new_section(self) -> AccountCampaignSelection | None:
        mcc_id = get_state(State.COMPANY)[f'{self._source_join}_id']
        accounts = dim_service.get_accounts(self._source_join, mcc_id)

        columns = st.columns(2)
        selected_account = columns[0].selectbox(
            "Account name",
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
        )

        campaigns = []
        if selected_account:
            campaigns = ["__ALL__"] + dim_service.get_campaigns(self._source_join, selected_account.account_id)
        selected_campaign = columns[1].selectbox(
            "Campaign name",
            options=campaigns,
            format_func=lambda m: "All campaigns" if m == "__ALL__" else m.campaign_name,
            index=None,
        )

        if all([selected_account, selected_campaign]):
            return AccountCampaignSelection(
                account=selected_account,
                campaign_mapping=None if selected_campaign == "__ALL__" else selected_campaign,
                active=True,
            )
        return None
