import warnings
from collections import defaultdict
from typing import List

import pandas as pd

from components.filter_dataframe import filteref_df

warnings.simplefilter(action='ignore', category=FutureWarning)
import confiugrations

import streamlit as st
import streamlit_antd_components as sac
from enum import Enum, auto


class StateKey(Enum):
    EDITING_ENABLED = auto()



def get_data(conn, table):
    df = conn.query(f"select * from {table} limit 10", ttl=60)
    return df


services = {
    "google-postbacker": {
        "display_name": "Google Postbacker",
        "mysql_conn": None,
        "tables": {
            "gradual_rollout_site_configuration": {
                "column_order": [],
                "column_config": {}
            },
            "gradual_rollout_configuration": {
                "column_order": [],
                "column_config": {}
            },
        }
    },
    "resolver": {
        "display_name": "Resolver",
        "mysql_conn": None,
        "tables": {
            "partner_timezone_mapping": {
                "column_order": [],
                "column_config": {}
            },
            "google_account_campaign_mappings": {
                "column_order": [],
                "column_config": {}
            },
            "s2s_deal_type_mapping": {
                "column_order": [
                    "s2s_action_deal_type",
                    "resolver_deal_type",
                    "partner"
                ],
                "column_config": {
                    "s2s_action_deal_type": st.column_config.TextColumn(required=True),
                    "resolver_deal_type": st.column_config.SelectboxColumn(
                        options=["Sale", "Lead"],
                        required=True
                    ),
                    "partner": st.column_config.TextColumn(required=True)
                }
            }
        }
    }
}


def toggle_state(key):
    st.session_state[key] = not st.session_state[key]


def get_state_key(configuration: str, key):
    return f"{configuration}:{key}"


def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


def init_state_editor_agg(state_key_data_editor_idx: str):
    init_state(state_key_data_editor_idx, {
        "edited_idxs": {},
        "added_idxs": pd.Series([]),
        "deleted_idxs": pd.Series([])
    })

@st.cache_resource(ttl=60)
def get_db_connections(configuration: str):
    conns = {}
    for table in confiugrations.all_by_name[configuration].tables:
        service = table['service']
        if service not in conns:
            conns[service] = st.experimental_connection(
                f"{service}_db",
                type="sql"
            )
    return conns


def setup_sidebar_controls():
    with st.sidebar.container():
        st.title("Configuration Service")
        st.divider()

        st.selectbox(
            label="Company:",
            options=["Natural Intelligence", "Cappsool", "Better Impression"],
            key="company"
        )

        configuration_choice = st.selectbox(
            label="Configuration:",
            options=confiugrations.all_by_name.keys(),
        )
        st.session_state["configuration"] = confiugrations.all_by_name[configuration_choice]


def setup_df_controls(configuration):
    control_btns_cols = st.columns((1, 6.8))

    state_key_editing_enabled = get_state_key(configuration.name, "editing_enabled")
    init_state(state_key_editing_enabled, False)
    button_text = "Enable editing" if not st.session_state[state_key_editing_enabled] else "Disable editing"
    button_type = "primary" if not st.session_state[state_key_editing_enabled] else "secondary"
    control_btns_cols[0].button(button_text, on_click=lambda: toggle_state(state_key_editing_enabled), type=button_type)

    state_key_filtering_enabled = get_state_key(configuration.name, "filtering_enabled")
    init_state(state_key_filtering_enabled, False)
    button_text = "Filter" if not st.session_state[state_key_filtering_enabled] else "Remove filters"
    button_type = "primary" if not st.session_state[state_key_filtering_enabled] else "secondary"
    control_btns_cols[1].button(button_text, on_click=lambda: toggle_state(state_key_filtering_enabled), type=button_type)


def debug_state():
    with st.sidebar.container():
        st.divider()
        st.write(st.session_state)


def main():
    st.set_page_config(layout="wide")

    setup_sidebar_controls()

    configuration = st.session_state["configuration"]
    st.title(configuration.name)
    setup_df_controls(configuration)
    conns = get_db_connections(configuration.name)

    # -------- display first table --------

    table = configuration.tables[0]
    df = get_data(conns[table['service']], table['name'])
    df.set_index("s2s_deal_type_mapping_id", inplace=True)
    # state_key_df = get_state_key(configuration.name, "df")
    # state_key_df_original = get_state_key(configuration.name, "df_original")
    # init_state(state_key_df_original, df)
    # init_state(state_key_df, df)

    if st.session_state[get_state_key(configuration.name, "filtering_enabled")]:
        df = filteref_df(df, choice_columns={"resolver_deal_type": ["Sale", "Lead"]})

    if not st.session_state[get_state_key(configuration.name, "editing_enabled")]:
        for key in ["data_editor", "data_editor_idx_agg"]:
            try:
                del st.session_state[get_state_key(configuration.name, key)]
            except KeyError:
                pass

    state_key_editor = get_state_key(configuration.name, "data_editor")
    state_key_data_editor_idx_agg = get_state_key(configuration.name, "data_editor_idx_agg")
    if state_key_data_editor_idx_agg in st.session_state or state_key_editor in st.session_state:
        init_state_editor_agg(state_key_data_editor_idx_agg)
        deleted_idxs_agg = st.session_state[state_key_data_editor_idx_agg]["deleted_idxs"]

        if state_key_editor in st.session_state:
            deleted_rows = st.session_state[state_key_editor]["deleted_rows"]
            if deleted_rows:
                cut_df = df.drop(deleted_idxs_agg)
                deleted_idxs_agg = pd.concat([deleted_idxs_agg,pd.Series(cut_df.iloc[deleted_rows].index)])
                st.session_state[state_key_data_editor_idx_agg]["deleted_idxs"] = deleted_idxs_agg

        df, deleted_rows_df = df.drop(deleted_idxs_agg), df.loc[deleted_idxs_agg]
        print(df)
        with st.expander("Rows to delete:", expanded=True):
            st.dataframe(
                deleted_rows_df,
                use_container_width=True,
                # hide_index=True,
                # column_order=table_settings['column_order'],
                # column_config=table_settings['column_config'],
            )

    # https://docs.streamlit.io/library/advanced-features/dataframes
    st.data_editor(
        df,
        use_container_width=True,
        # hide_index=True,
        disabled=not st.session_state[get_state_key(configuration.name, "editing_enabled")],
        num_rows="dynamic" if st.session_state[get_state_key(configuration.name, "editing_enabled")] else "fixed",
        # column_order=table_settings['column_order'],
        # column_config=table_settings['column_config'],
        key=state_key_editor
    )

    # f"df len: {len( st.session_state[state_key_df])}"

    st.write(st.session_state[state_key_editor])


main()
debug_state()