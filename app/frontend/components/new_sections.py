import streamlit as st

from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.dim_repository import dim_google_account_campaigns_mapping_repository, dim_google_account_repository


def account_and_allable_campaign_selection() -> tuple[GoogleAccount, bool, GoogleAccountCampaignMappings]:
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
    all_campaigns_checked = st.checkbox("All campaigns")
    selected_campaign = columns[1].selectbox(
        "Campaign name",
        options=get_campaigns(selected_account.account_id) if selected_account else [],

        # this is hack for when all_campaigns checked after a campaign was selected
        format_func=lambda m: m.campaign_name if not all_campaigns_checked else "",
        index=None,
        disabled=all_campaigns_checked,
    )

    return selected_account, all_campaigns_checked, selected_campaign
