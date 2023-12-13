from collections import defaultdict
from dataclasses import dataclass

import pandas as pd
import streamlit as st

from app.frontend.confiugration import BaseConfigurationFrontend
from app.frontend.confiugration import Selection
from model.configuration.google_parallel_predictions import DealType
from model.dim.google_account import GoogleAccount
from model.dim.partner import Partner
from repository.dim_repository import dim_google_account_repository, dim_partner_repository


@dataclass
class GoogleParallelPredictionsSelection(Selection):
    account: GoogleAccount
    partner: Partner
    deal_type: DealType
    active: bool


class GoogleParallelPredictionsFrontend(BaseConfigurationFrontend[GoogleParallelPredictionsSelection]):

    def __init__(self):
        super().__init__(
            label="Google - Parallel Predictions",
            display_name_mapping={
                "account_name": "Account name",
                "name": "Partner name",
                "deal_type": "Deal type",
            },
            enum_columns=["deal_type"],
        )

    def render_new_section(self) -> GoogleParallelPredictionsSelection | None:
        accounts = dim_google_account_repository.get()  # TODO only for current company
        partners = dim_partner_repository.get()  # TODO only for current company

        columns = st.columns(3)
        selected_account = columns[0].selectbox(
            "Account name",
            options=accounts,
            format_func=lambda a: a.account_name,
            index=None,
        )
        selected_partner = columns[1].selectbox(
            "Partner name",
            options=partners,  # TODO do we have a mapping somewhere?
            format_func=lambda p: p.name,
            index=None,
        )
        selected_deal_type = columns[2].selectbox(
            "Deal type",
            options=list(DealType),
            format_func=lambda d: d.value,
            index=None,
        )

        if all([selected_account, selected_partner]):
            return GoogleParallelPredictionsSelection(
                account=selected_account,
                partner=selected_partner,
                deal_type=selected_deal_type,
                active=True,
            )
        return None

    def create_df_from_selections(self, selections: list[GoogleParallelPredictionsSelection]) -> pd.DataFrame:
        selections_flattened = defaultdict(list)
        for selection in selections:
            selection_flattened = {}
            selection_flattened.update(selection.account.as_dict())
            selection_flattened.update(selection.partner.as_dict())
            selection_flattened['deal_type'] = selection.deal_type
            selection_flattened['active'] = selection.active
            for k, v in selection_flattened.items():
                selections_flattened[k].append(v)
        return pd.DataFrame(selections_flattened)
