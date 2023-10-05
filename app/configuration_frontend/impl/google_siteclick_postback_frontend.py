import streamlit as st

from ..base_configuration_frontend import BaseConfigurationFrontend


class GoogleSiteclickPostbackFrontend(BaseConfigurationFrontend):

    def __init__(self):
        super().__init__(
            name="Google - Siteclick Postback",
            display_name_mapping={
                "mcc_id": "MCC ID",
                "account_id": "Account ID",
                "campaign_id": "Campaign ID",
            }
        )

    def render_new_section(self): # TODO
        pass
