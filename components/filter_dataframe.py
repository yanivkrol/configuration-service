import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_numeric_dtype
)


def filter_df(
        df: pd.DataFrame,
        column_order: list = None,
        choice_columns=None
) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe
        choice_columns: mapping between column that have choices and the possible values

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    if column_order is None:
        column_order = df.columns
    if choice_columns is None:
        choice_columns = {}

    df = df.copy()

    with st.sidebar.container():
        st.write("Filters:")
        # columns_to_filter = st.multiselect("filters", df.columns,
        #                                    placeholder="Columns to filter...",
        #                                    label_visibility="collapsed")
        for column in column_order:
            if column in choice_columns:
                user_choice_input = st.multiselect(
                    f"Values for {column}",
                    choice_columns[column],
                )
                if user_choice_input:
                    df = df[df[column].isin(user_choice_input)]

            else:
                user_text_input = st.text_input(f"Substring in {column}")
                if user_text_input:
                    user_text_input = user_text_input.strip()
                    if is_numeric_dtype(df[column]):
                        df = df[df[column] == int(user_text_input)]
                    else:
                        df = df[df[column].str.contains(user_text_input.strip(), case=False, regex=False)]

    return df
