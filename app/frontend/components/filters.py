from datetime import time
from typing import Protocol, Literal

import pandas as pd
import streamlit as st


class ColumnFilter(Protocol):
    def filter(self, unfiltered_df: pd.DataFrame, filtered_df: pd.DataFrame, disabled: bool = False) -> pd.DataFrame:
        ...


class AllableCampaignFilter(ColumnFilter):
    def filter(self, unfiltered_df: pd.DataFrame, filtered_df: pd.DataFrame, disabled: bool = False) -> pd.DataFrame:
        options = list(unfiltered_df["campaign_name"].unique())
        try:
            options.remove(None)
            options.insert(0, None)
        except ValueError:
            pass
        selected = st.multiselect(
            "Campaign name:",
            options,
            format_func=lambda o: o or "All campaigns",
            default=[],
            disabled=disabled,
        )
        if selected:
            filtered_df = filtered_df[filtered_df["campaign_name"].isin(selected)]

        return filtered_df


Relativity = Literal["from", "to"]


class DatetimeFilter(ColumnFilter):

    def __init__(self, relativity: Relativity):
        if relativity not in list(Relativity.__args__):
            raise ValueError(f"relativity must be in {list(Relativity)}")
        self._relativity = relativity

    def filter(self, unfiltered_df: pd.DataFrame, filtered_df: pd.DataFrame, disabled: bool = False) -> pd.DataFrame:
        columns = st.columns(2)
        selected_from = columns[0].date_input(
            f"Date {self._relativity}",
            disabled=disabled,
        )
        selected_from = columns[1].time_input(
            f"Time {self._relativity}",
            value=time(),
            disabled=disabled,
        )

        return filtered_df  # TODO actually filter
