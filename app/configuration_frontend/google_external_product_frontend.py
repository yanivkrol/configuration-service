from collections import defaultdict
from dataclasses import dataclass

import pandas as pd
import streamlit as st

from app.configuration_frontend import BaseConfigurationFrontend
from app.configuration_frontend import Selection
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from repository.dim_repository import dim_google_account_campaigns_mapping_repository, dim_google_account_repository


@dataclass
class GoogleExternalProductSelection(Selection):
    account: GoogleAccount
    campaign_mapping: GoogleAccountCampaignMappings
    active: bool = True


class GoogleExternalProductFrontend(BaseConfigurationFrontend[GoogleExternalProductSelection]):

    def __init__(self):
        super().__init__(
            label="Google - External Product",
            display_name_mapping={
                "account_name": "Account Name",
                "campaign_name": "Campaign Name",
            },
            custom_filter_columns=["campaign_name"]
        )

    def get_df_for_display(self, df) -> pd.DataFrame:
        df = super().get_df_for_display(df)
        df['campaign_name'] = df['campaign_name'].apply(lambda c: c or "All campaigns")
        return df

    def _render_custom_filter(self, unfiltered_df: pd.DataFrame, filtered_df: pd.DataFrame,
                              column: str) -> pd.DataFrame:
        if column == "campaign_name":
            options = list(unfiltered_df[column].unique())
            try:
                options.remove(None)
                options.insert(0, None)
            except ValueError:
                pass
            selected = st.multiselect(
                f"{self.display_name_mapping[column]}:",
                options,
                format_func=lambda o: o or "All campaigns",
                default=[]
            )
            if selected:
                filtered_df = filtered_df[filtered_df[column].isin(selected)]

        return filtered_df

    def render_new_section(self) -> GoogleExternalProductSelection | None:
        account_campaign_mappings = dim_google_account_campaigns_mapping_repository.get()
        accounts = dim_google_account_repository.get()

        def get_campaigns(account_id):
            return [m for m in account_campaign_mappings if m.account_id == account_id]

        columns = st.columns(2)
        selected_account = columns[0].selectbox(
            "Account Name",
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
        )
        all_campaigns_checked = st.checkbox("All campaigns")
        selected_campaign = columns[1].selectbox(
            "Campaign Name",
            options=get_campaigns(selected_account.account_id) if selected_account else [],

            # this is hack for when all_campaigns checked after a campaign was selected
            format_func=lambda m: m.campaign_name if not all_campaigns_checked else "",
            index=None,
            disabled=all_campaigns_checked,
        )

        if all([selected_account, all_campaigns_checked or selected_campaign]):
            return GoogleExternalProductSelection(
                account=selected_account,
                campaign_mapping=None if all_campaigns_checked else selected_campaign
            )
        return None

    def create_df_from_selections(self, selections: list[GoogleExternalProductSelection]) -> pd.DataFrame:
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
