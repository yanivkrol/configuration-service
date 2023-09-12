import streamlit as st

from ..base_configuration_frontend import BaseConfigurationFrontend


class GoogleSiteclickPostbackFrontend(BaseConfigurationFrontend):

    def __init__(self):
        super().__init__(
            name="Google - Siteclick Postback",
            column_order=[
                "mcc_id",
                "account_id",
                "campaign_id"
            ],
            column_config={
                "mcc_id": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                ),
                "account_id": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                ),
                "campaign_id": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                )
            }
        )
