import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
import streamlit_antd_components as sac
from enum import Enum, auto


class StateKey(Enum):
    EDITING_ENABLED = auto()



def get_all(conn, table):
    df = conn.query(f"select * from {table} limit 50", ttl=60)
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


def get_state_key(service, table, key):
    return f"{service}:{table}:{key}"

def main():
    st.set_page_config(layout="wide")

    for service, service_settings in services.items():
        service_settings['mysql_conn'] = st.experimental_connection(
            f"{service.replace('-', '_')}_db",
            type="sql"
        )

    menu_items = []
    for service, service_settings in services.items():
        children = []
        for table in service_settings['tables'].keys():
            children.append(sac.MenuItem(f'{service}:{table}', icon='database'))
        menu_items.append(sac.MenuItem(service_settings['display_name'], icon='gear', children=children))

    with st.sidebar.container():
        st.title("Configuration Service")
        selected = sac.menu(menu_items, index=0, size='small', indent=12,
                            open_index=None, open_all=True, return_index=False,
                            format_func=lambda s: s.split(":")[-1])

    if ":" in selected:
        service, table = selected.split(":")
        service_settings = services[service]
        table_settings = service_settings['tables'][table]
        st.title(f"{service_settings['display_name']} - {table}")
        df = get_all(service_settings['mysql_conn'], table)
        state_key_df = get_state_key(service, table, "df")
        if state_key_df not in st.session_state:
            st.session_state[state_key_df] = df

        state_key_editing_enabled = get_state_key(service, table, "editing_enabled")
        if state_key_editing_enabled not in st.session_state:
            st.session_state[state_key_editing_enabled] = False
        button_text = "Enabled editing" if not st.session_state[state_key_editing_enabled] else "Disable editing"
        st.button(button_text, on_click=lambda: toggle_state(state_key_editing_enabled))

        state_key_editor = get_state_key(service, table, "data_editor")
        if state_key_editor in st.session_state:
            deleted_rows = st.session_state[state_key_editor]["deleted_rows"]
            if deleted_rows:
                with st.expander("Deleted rows:", expanded=True):
                    st.dataframe(
                        st.session_state[state_key_df].iloc[deleted_rows],
                        use_container_width=True,
                        hide_index=True,
                        column_order=table_settings['column_order'],
                        column_config=table_settings['column_config'],
                    )

        # https://docs.streamlit.io/library/advanced-features/dataframes
        st.session_state[state_key_df] = st.data_editor(
            st.session_state[state_key_df],
            use_container_width=True,
            hide_index=True,
            disabled=not st.session_state[state_key_editing_enabled],
            num_rows="dynamic" if st.session_state[state_key_editing_enabled] else "fixed",
            column_order=table_settings['column_order'],
            column_config=table_settings['column_config'],
            key=state_key_editor
        )

        f"df len: {len( st.session_state[state_key_df])}"

        st.write(st.session_state[state_key_editor])


main()





# def show_ui():
#     st.sidebar.title('Configuration')
#     st.sidebar.
#     service = st.sidebar.selectbox('Choose Service', ['Service 1', 'Service 2'])
#     table = st.sidebar.selectbox('Choose Table', ['users', 'another_table'])
#
#     st.title(f'{service} - {table}')
#
#     df = read_table(table)
#     st.write(df)
#
# import pandas as pd
#
# def read_table(table_name):
#     conn = sqlite3.connect('example.db')
#     df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
#     conn.close()
#     return df
#
#
# show_ui()