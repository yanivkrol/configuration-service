import warnings
from time import sleep

from components.filter_dataframe import filter_df
from configuration.configuration import Configuration
from state_management import *

warnings.simplefilter(action='ignore', category=FutureWarning)
import confiugrations

import streamlit as st


def get_data(conn, table):
    df = conn.query(f"select * from {table} limit 10", ttl=60)
    return df


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


def something_changed():
    data_editor = get_state(State.DATA_EDITOR)
    return data_editor and bool(data_editor["edited_rows"] or data_editor["deleted_rows"])


# ------------------ start ------------------


st.set_page_config(layout="wide")

# ------------------ sidebar ------------------


with st.sidebar.container():
    # remove margin
    st.markdown("""
      <style>
        .css-10oheav.eczjsme4 {
          margin-top: -75px;
        }
      </style>
    """, unsafe_allow_html=True)

    st.title("Configuration Service")
    st.divider()

    st.selectbox(
        label="Company:",
        options=["Natural Intelligence", "Cappsool", "Better Impression"],
        key=State.COMPANY
    )

    configuration_choice = st.selectbox(
        label="Configuration:",
        options=confiugrations.all_by_name.keys(),
    )
    set_state(State.CONFIGURATION, confiugrations.all_by_name[configuration_choice])

    st.divider()

# ------------------ start main section ------------------


configuration: Configuration = get_state(State.CONFIGURATION)

if not get_state(State.EDITING_ENABLED):
    del_state(State.DATA_EDITOR)

st.title(configuration.name)

# ------------------ control buttons ------------------


control_btns_cols = st.columns((1, 8))

save_btn = control_btns_cols[1].button("Save", type="primary", disabled=not something_changed())
if save_btn:
    with st.spinner("Saving..."):
        sleep(1)  # TODO actually save data
        del_state(State.DATA_EDITOR)  # TODO Maybe redundant once fresh data is fetched
        set_state(State.EDITING_ENABLED, False)
        st.success("Saved successfully!", icon="🚀")

init_state(State.EDITING_ENABLED, False)
button_text = "Enable editing" if not get_state(State.EDITING_ENABLED) else "Disable editing"
button_type = "primary" if not get_state(State.EDITING_ENABLED) else "secondary"
control_btns_cols[0].button(button_text, type=button_type, on_click=lambda: toggle_state(State.EDITING_ENABLED))

# TODO below code is with confirmation
# init_state(State.SAVE_CLICKED, False)
# init_state(State.SAVE_CONFIRMED, False)
# control_btns_cols[1].button("Save", type="primary",
#                             disabled=not something_changed(),
#                             on_click=lambda: set_state(State.SAVE_CLICKED, True))
#
# if get_state(State.SAVE_CLICKED):
#     set_state(State.SAVE_CLICKED, False)
#     # TODO maybe Modal (not officially released yet https://experimental-modals.streamlit.app/)
#     # TODO possible to use https://pypi.org/project/streamlit-modal/ in the meanwhile
#     st.write("You are about to apply the changes. Please review them before continuing.")
#     col1, col2 = st.columns((1, 15))
#     col1.button("Cancel", type="secondary")
#     col2.button("Continue", type="primary", on_click=lambda: set_state(State.SAVE_CONFIRMED, True))
#
# if get_state(State.SAVE_CONFIRMED):
#     set_state(State.SAVE_CONFIRMED, False)
#     with st.spinner("Saving..."):
#     del_state(State.DATA_EDITOR)  # TODO Maybe redundant once fresh data is fetched
#     st.success("Saved successfully!", icon="🚀")


# -------- display first table --------


conns = get_db_connections(configuration.name)
table = configuration.tables[0]  # TODO multiple tables
df = get_data(conns[table['service']], table['name'])
df.rename(columns={configuration.id_column: "id"}, inplace=True)
df.set_index("id", inplace=True)

df = filter_df(df,
               column_order=configuration.column_order,
               choice_columns=configuration.filter_column_choices)

# ---------------- display changes ----------------


if something_changed():
    deleted_rows = get_state(State.DATA_EDITOR)["deleted_rows"]
    if deleted_rows:
        deleted_idxs = df.iloc[deleted_rows].index
        deleted_rows_df = df.loc[deleted_idxs]
        with st.expander("Deleted rows:", expanded=True):
            st.dataframe(
                deleted_rows_df,
                use_container_width=True,
                column_order=configuration.column_order,
                column_config=configuration.column_config,
            )

    edited_rows = get_state(State.DATA_EDITOR)["edited_rows"]
    if edited_rows:
        edited_idxs = df.iloc[map(int, edited_rows.keys())].index
        edited_rows_df = df.loc[edited_idxs]
        with st.expander("Edited rows (Showing original values):", expanded=True):
            st.dataframe(
                edited_rows_df,
                use_container_width=True,
                column_order=configuration.column_order,
                column_config=configuration.column_config,
            )

    # Don't allow adding rows directly to the dataframe
    added_rows = get_state(State.DATA_EDITOR)["added_rows"]
    if added_rows:
        st.warning("Adding rows directly to the dataframe is not supported. " +
                   "Any changes will not be saved.")

# ------------------ data editor ------------------

# https://docs.streamlit.io/library/advanced-features/dataframes
st.data_editor(
    df,
    use_container_width=True,
    column_order=configuration.column_order,
    column_config=configuration.column_config,
    disabled=not get_state(State.EDITING_ENABLED),
    num_rows="dynamic" if get_state(State.EDITING_ENABLED) else "fixed",
    key=State.DATA_EDITOR
)


def debug_state():
    col1, col2 = st.columns((1, 3))
    col1.write(get_state(State.DATA_EDITOR))
    col2.write(st.session_state)


debug_state()
