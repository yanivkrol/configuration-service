import sys
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

import pandas as pd
import streamlit as st

from configurations import ConfigurationId


class Selection(ABC):
    pass


SelectionT = TypeVar('SelectionT', bound=Selection)


class BaseConfigurationFrontend(ABC, Generic[SelectionT]):

    def __init__(self,
                 label: str,
                 display_name_mapping: dict[str, str],
                 custom_filter_columns: Optional[list[str]] = None):
        self.label = label

        self.column_config = {'id': st.column_config.NumberColumn(
            label="ID",
        )}
        self.column_config.update({
            column: st.column_config.TextColumn(
                label=display_name,
                disabled=True,  # No editing values for now, only active/inactive
            )
            for column, display_name in display_name_mapping.items()
        })
        self.column_config['active'] = st.column_config.CheckboxColumn(
            label="Active",
            width="small",
        )

        self.column_order = list(self.column_config.keys())
        self.column_order.remove("id")

        self.display_name_mapping = {k: cfg['label'] for k, cfg in self.column_config.items()}
        self.display_name_mapping.pop("id")

        self.custom_filter_columns = custom_filter_columns or []

    def get_df_for_display(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.copy()

    def render_filters(self, unfiltered_df: pd.DataFrame, disabled: bool = False) -> pd.DataFrame:
        filtered_df = unfiltered_df  # Any filtering is not in place, so we iteratively work on 'filtered_df'

        for column in self.column_order:
            if column in self.custom_filter_columns:
                filtered_df = self._render_custom_filter(unfiltered_df, filtered_df, column, disabled=disabled)

            elif column == "active":
                selected = st.radio(
                    "Active:",
                    ("All", "Yes", "No"),
                    horizontal=True,
                    disabled=disabled,
                )
                if selected == "Yes":
                    filtered_df = filtered_df[filtered_df["active"] == True]
                elif selected == "No":
                    filtered_df = filtered_df[filtered_df["active"] == False]

            else:
                selected = st.multiselect(
                    f"{self.display_name_mapping[column]}:",
                    unfiltered_df[column].unique(),
                    disabled=disabled,
                )
                if selected:
                    filtered_df = filtered_df[filtered_df[column].isin(selected)]

        if filtered_df is unfiltered_df:
            return unfiltered_df.copy()
        return filtered_df

    def _render_custom_filter(self, unfiltered_df: pd.DataFrame, filtered_df: pd.DataFrame,
                              column: str, disabled: bool = False) -> pd.DataFrame:
        return filtered_df

    @abstractmethod
    def render_new_section(self) -> SelectionT | None:
        ...

    @abstractmethod
    def create_df_from_selections(self, selections: list[SelectionT]) -> pd.DataFrame:
        ...


from app.frontend.confiugration.google_external_product_frontend import GoogleExternalProductFrontend
from app.frontend.confiugration.google_siteclick_postback_frontend import GoogleSiteclickPostbackFrontend

_google_external_product_frontend = GoogleExternalProductFrontend()
_google_siteclick_postback_frontend = GoogleSiteclickPostbackFrontend()


def get_frontend(config_id: ConfigurationId) -> BaseConfigurationFrontend:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_frontend')
