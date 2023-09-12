import streamlit as st

from ..base_configuration_frontend import BaseConfigurationFrontend


class GoogleExternalProductFrontend(BaseConfigurationFrontend):

    def __init__(self):
        super().__init__(
            name="Google - External Product",
            column_config={
                "account_id": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                ),
                "campaign_id": st.column_config.TextColumn(
                    required=True,
                    validate="[a-zA-Z0-9_\\-]+",
                ),
                "external_partner_product_naming_enabled": st.column_config.CheckboxColumn(
                    default=False,
                )
            },
            create_fields_config={
                "account_id": lambda: st.text_input("Account ID"),
                "campaign_id": lambda: st.text_input("Campaign ID"),
                "external_partner_product_naming_enabled": lambda: st.checkbox("External Partner Product Naming Enabled")
            }
        )
