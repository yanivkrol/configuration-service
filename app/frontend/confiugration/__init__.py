import sys
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

import pandas as pd
import streamlit as st

from app.frontend.components.filters import ColumnFilter
from common.configurations import ConfigurationId


class Selection(ABC):
    pass


SelectionT = TypeVar('SelectionT', bound=Selection)


class BaseConfigurationFrontend(ABC, Generic[SelectionT]):

    def __init__(self,
                 label: str,
                 display_name_mapping: dict[str, str],
                 custom_column_filters: Optional[dict[str, ColumnFilter]] = None,
                 custom_column_display_function: Optional[dict[str, callable]] = None,
                 enum_columns: Optional[list[str]] = None):
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

        self.custom_filter_columns = custom_column_filters or []
        self.custom_column_display_function = custom_column_display_function or {}
        self.enum_columns = enum_columns or []

    def get_df_for_display(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for column in self.enum_columns:
            df[column] = df[column].apply(lambda enum: enum.value)
        for column, function in self.custom_column_display_function.items():
            df[column] = function(df[column])

        return df

    def render_filters(self, unfiltered_df: pd.DataFrame, disabled: bool = False) -> pd.DataFrame:
        filtered_df = unfiltered_df  # Any filtering is not in place, so we iteratively work on 'filtered_df'

        for column in self.column_order:
            if column in self.custom_filter_columns:
                filtered_df = self.custom_filter_columns[column].filter(unfiltered_df, filtered_df, disabled=disabled)

            elif column == "active":  # TODO bug: the state remains between different high-level selections
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
                    format_func=(lambda enum: enum.value) if (column in self.enum_columns) else (lambda x: x),
                    disabled=disabled,
                )
                if selected:
                    filtered_df = filtered_df[filtered_df[column].isin(selected)]

        if filtered_df is unfiltered_df:
            return unfiltered_df.copy()
        return filtered_df

    @abstractmethod
    def render_new_section(self) -> SelectionT | None:
        ...


from .bing_postback_with_commission_frontend import BingPostbackWithCommissionFrontend
from .google_active_postback_frontend import GoogleActivePostbackFrontend
from .google_external_product_frontend import GoogleExternalProductFrontend
from .google_siteclick_postback_frontend import GoogleSiteclickPostbackFrontend
from .google_parallel_predictions_frontend import GoogleParallelPredictionsFrontend
from .google_postback_with_commission_frontend import GooglePostbackWithCommissionFrontend

_bing_postback_with_commission_frontend = BingPostbackWithCommissionFrontend()
_google_active_postback_frontend = GoogleActivePostbackFrontend()
_google_external_product_frontend = GoogleExternalProductFrontend()
_google_siteclick_postback_frontend = GoogleSiteclickPostbackFrontend()
_google_parallel_predictions_frontend = GoogleParallelPredictionsFrontend()
_google_postback_with_commission_frontend = GooglePostbackWithCommissionFrontend()


def get_frontend(config_id: ConfigurationId) -> BaseConfigurationFrontend:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_frontend')
