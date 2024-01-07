from typing import Literal

import streamlit as st

from app.frontend.state_management import get_state, State
from app.middleware.dim_service import DimensionsService
from model.dim.account import Account
from model.dim.account_campaign_mapping import AccountCampaignMapping


def account_and_allable_campaign_selection(source_join: str) -> tuple[Account, AccountCampaignMapping | Literal["__ALL__"]]:
    dim_service = DimensionsService()
    mcc_id = get_state(State.COMPANY)[f'{source_join}_id']
    accounts = dim_service.get_accounts(source_join, mcc_id)

    columns = st.columns(2)
    selected_account = columns[0].selectbox(
        "Account name",
        options=accounts,
        format_func=lambda a: a.account_name,
        index=None,
    )

    campaigns = []
    if selected_account:
        campaigns = ["__ALL__"] + dim_service.get_campaigns(source_join, selected_account.account_id)
    selected_campaign = columns[1].selectbox(
        "Campaign name",
        options=campaigns,
        format_func=lambda m: "All campaigns" if m == "__ALL__" else m.campaign_name,
        index=None,
    )

    return selected_account, selected_campaign
