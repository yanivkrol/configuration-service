import streamlit as st

from repository.dim_repository import dim_google_account_campaigns_mapping_repository, dim_google_account_repository
from ..base_configuration_frontend import BaseConfigurationFrontend


class GoogleExternalProductFrontend(BaseConfigurationFrontend):

    def __init__(self):
        super().__init__(
            name="Google - External Product",
            display_name_mapping={
                "account_name": "Account Name",
                "campaign_id": "Campaign ID",
            }
        )

    def render_new_section(self):
        account_campaign_mappings = dim_google_account_campaigns_mapping_repository.get()
        accounts = dim_google_account_repository.get()

        def get_campaigns(account_id):
            return list(filter(lambda m: m.account_id == account_id, account_campaign_mappings))

        columns = st.columns(2)
        selected_account = columns[0].selectbox(
            self.display_name_mapping['account_name'],
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
            key="add_new_account"
        )
        columns[1].selectbox(
            self.display_name_mapping['campaign_id'],
            options=get_campaigns(selected_account.account_id) if selected_account else [],
            format_func=lambda c: c.campaign_name,
            index=None,
            key="add_new_campaign"
        )
