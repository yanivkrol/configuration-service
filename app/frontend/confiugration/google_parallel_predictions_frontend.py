from dataclasses import dataclass

import streamlit as st

from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from app.state_management import get_state, State
from app.middleware.dim_service import dim_service
from common.model.configuration.google_parallel_predictions import DealType
from common.model.dim.account import Account
from common.model.dim.partner import Partner


@dataclass
class GoogleParallelPredictionsSelection(Selection):
    account: Account
    partner: Partner
    deal_type: DealType
    active: bool


class GoogleParallelPredictionsFrontend(BaseConfigurationFrontend[GoogleParallelPredictionsSelection]):

    def __init__(self):
        super().__init__(
            label="Google - Parallel Predictions",
            display_name_mapping={
                "account_name": "Account name",
                "partner_name": "Partner name",
                "deal_type": "Deal type",
            },
            enum_columns=["deal_type"],
        )

    def render_new_section(self) -> GoogleParallelPredictionsSelection | None:
        company = get_state(State.COMPANY)
        source_join = 'google'
        accounts = dim_service.get_accounts(source_join, company[f'{source_join}_id'])
        partners = dim_service.get_partners(company['shortened'])

        columns = st.columns(3)
        selected_account = columns[0].selectbox(
            "Account name",
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
        )
        selected_partner = columns[1].selectbox(
            "Partner name",
            options=partners,
            format_func=lambda p: p.name,
            index=None,
        )
        selected_deal_type = columns[2].selectbox(
            "Deal type",
            options=list(DealType),
            format_func=lambda d: d.value,
            index=None,
        )

        if all([selected_account, selected_partner, selected_deal_type]):
            return GoogleParallelPredictionsSelection(
                account=selected_account,
                partner=selected_partner,
                deal_type=selected_deal_type,
                active=True,
            )
        return None

    def _to_display_dict(self, selection: GoogleParallelPredictionsSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'partner_name': selection.partner.name,
            'deal_type': selection.deal_type,
            'active': selection.active,
        }
