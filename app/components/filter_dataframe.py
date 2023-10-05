import pandas as pd
import streamlit as st

from app.configuration_frontend import BaseConfigurationFrontend


def filter_df(
        df: pd.DataFrame,
        config_frontend: BaseConfigurationFrontend,
) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe
        choice_columns: mapping between column that have choices and the possible values

    Returns:
        pd.DataFrame: Filtered dataframe
        :param config_frontend:
    """
    df_original = df
    df = df.copy()

    with st.sidebar.container():
        st.write("Filters:")
        # columns_to_filter = st.multiselect("filters", df.columns,
        #                                    placeholder="Columns to filter...",
        #                                    label_visibility="collapsed")
        for column in config_frontend.column_order:
            if column == "active":
                selected = st.radio(
                    "State",
                    ("Active", "Inactive", "All"),
                    index=2,
                    horizontal=True,
                )
                if selected == "Active":
                    df = df[df["active"] == True]
                elif selected == "Inactive":
                    df = df[df["active"] == False]

            else:
                user_choice_input = st.multiselect(
                    f"{config_frontend.display_name_mapping[column]}:",
                    df_original[column].unique(),
                )
                if user_choice_input:
                    df = df[df[column].isin(user_choice_input)]
                # user_text_input = st.text_input(f"Substring in {column}", autocomplete="default")
                # if user_text_input:
                #     user_text_input = user_text_input.strip()
                #     if is_numeric_dtype(df[column]):
                #         df = df[df[column] == int(user_text_input)]
                #     else:
                #         df = df[df[column].str.contains(user_text_input.strip(), case=False, regex=False)]

    return df
