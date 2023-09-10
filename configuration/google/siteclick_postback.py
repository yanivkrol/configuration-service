from configuration.configuration import Configuration
import streamlit as st


class GoogleSiteclickPostback(Configuration):

    def __init__(self):
        super().__init__(
            name="Google - Siteclick Postback",
            id_column="s2s_deal_type_mapping_id",
            tables=[
                {
                    "service": "resolver",
                    "name": "s2s_deal_type_mapping"
                }
            ],
            column_order=[
                "s2s_action_deal_type",
                "resolver_deal_type",
                "partner"
            ],
            filter_column_choices={
                "resolver_deal_type": ["Sale", "Lead"]
            },
            column_config={
                "s2s_action_deal_type": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                ),
                "resolver_deal_type": st.column_config.SelectboxColumn(
                    required=True,
                    options=["Sale", "Lead"],
                ),
                "partner": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                )
            }
        )
