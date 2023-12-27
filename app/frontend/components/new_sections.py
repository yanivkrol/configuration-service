from typing import Literal

import streamlit as st

from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.dim_repository import dim_google_account_campaigns_mapping_repository, dim_google_account_repository


def account_and_allable_campaign_selection() -> tuple[GoogleAccount, GoogleAccountCampaignMappings | Literal["__ALL__"]]:
    account_campaign_mappings = dim_google_account_campaigns_mapping_repository.get()  # TODO only for current company
    accounts = dim_google_account_repository.get()  # TODO only for current company

    def get_campaigns(account_id):
        return [m for m in account_campaign_mappings if m.account_id == account_id]

    columns = st.columns(2)
    selected_account = columns[0].selectbox(
        "Account name",
        options=accounts,
        format_func=lambda a: a.account_name,
        index=None,
    )

    campaigns = ["__ALL__"] + get_campaigns(selected_account.account_id) if selected_account else []
    selected_campaign = columns[1].selectbox(
        "Campaign name",
        options=campaigns,
        format_func=lambda m: "All campaigns" if m == "__ALL__" else m.campaign_name,
        index=None,
    )

    return selected_account, selected_campaign
