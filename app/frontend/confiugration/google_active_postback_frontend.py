from dataclasses import dataclass

import streamlit as st

from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from app.middleware.dim_service import dim_service
from app.state_management import get_state, State
from common.model.configuration.google_active_postback import TrafficJoin
from common.model.dim.account import Account
from common.model.dim.site import Site
from common.model.dim.vertical import Vertical


@dataclass
class GoogleActivePostbackSelection(Selection):
    account: Account
    site: Site
    vertical: Vertical
    traffic_join: TrafficJoin
    active: bool


class GoogleActivePostbackFrontend(BaseConfigurationFrontend[GoogleActivePostbackSelection]):

    def __init__(self):
        super().__init__(
            label="Google - Active Postback",
            display_name_mapping={
                "account_name": "Account name",
                "site_name": "Site name",
                "vertical_name": "Vertical name",
                "traffic_join": "Traffic join",
            },
            enum_columns=["traffic_join"],
        )

    def render_new_section(self) -> GoogleActivePostbackSelection | None:
        company = get_state(State.COMPANY)
        source_join = 'google'
        accounts = dim_service.get_accounts(source_join, company[f'{source_join}_id'])
        sites = dim_service.get_sites()

        columns = st.columns(4)
        selected_account = columns[0].selectbox(
            "Account name",
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
        )
        selected_traffic_join = columns[1].selectbox(
            "Traffic join",
            options=list(TrafficJoin),
            format_func=lambda t: t.value,
            index=None,
        )
        selected_site = columns[2].selectbox(
            "Site name",
            options=sites,
            format_func=lambda s: s.name,
            index=None,
        )
        selected_vertical = columns[3].selectbox(
            "Vertical name",
            options=dim_service.get_site_verticals(selected_site.id) if selected_site else [],
            format_func=lambda v: v.name,
            index=None,
        )

        if all([selected_account, selected_traffic_join, selected_site, selected_vertical]):
            return GoogleActivePostbackSelection(
                account=selected_account,
                site=selected_site,
                vertical=selected_vertical,
                traffic_join=selected_traffic_join,
                active=True,
            )
        return None

    def _to_display_dict(self, selection: GoogleActivePostbackSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'site_name': selection.site.name,
            'vertical_name': selection.vertical.name,
            'traffic_join': selection.traffic_join,
            'active': selection.active,
        }
