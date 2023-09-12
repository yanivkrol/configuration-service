import warnings

from configuration_frontend.base_configuration_frontend import BaseConfigurationFrontend
from configurations import get_all_configurations

warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st

st.set_page_config(layout="wide")
# this must be called before any Streamlit commands
# we call a command in BaseRepository.__init()__ so we need to call it here before the import
# It is not a must to work with streamlit database connection, could be done through regular sqlalchemy connection

import process_changes

import configuration_frontend
import repository.configuration_repository as configuration_repository
from repository.configuration_repository import ConfigurationRepository
from components.filter_dataframe import filter_df
from state_management import *


def is_data_edited():
    data_editor = get_state(State.DATA_EDITOR)
    return data_editor and bool(data_editor["edited_rows"] or data_editor["deleted_rows"])


def load_df(c_frontend: BaseConfigurationFrontend, c_repository: ConfigurationRepository):
    df = c_repository.get_as_df(limit=10, ttl=0)
    df = filter_df(df,
                   column_order=c_frontend.column_order,
                   choice_columns=c_frontend.filter_column_choices)
    return df


init_default_states()
if not get_state(State.EDITING_ENABLED):
    reset_main_section_state()

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

    st.selectbox(
        label="Configuration:",
        options=get_all_configurations(),
        format_func=lambda x: configuration_frontend.get_frontend(x).name,
        on_change=reset_main_section_state,
        key=State.CONFIGURATION
    )

    st.divider()


# ------------------ start main section ------------------


c_frontend = configuration_frontend.get_frontend(get_state(State.CONFIGURATION))
c_repository = configuration_repository.get_repository(get_state(State.CONFIGURATION))

st.title(c_frontend.name)
df = load_df(c_frontend, c_repository)


# ------------------ control buttons ------------------


control_btns_cols = st.columns((1, 6))

save_btn = control_btns_cols[1].button("Save", type="primary", disabled=not is_data_edited())
if save_btn:
    with st.spinner("Saving..."):
        data_editor = get_state(State.DATA_EDITOR)
        process_changes.apply_changes(c_repository, df, data_editor["deleted_rows"], data_editor["edited_rows"])
        reset_main_section_state()
        st.success("Saved successfully!", icon="🚀")
        df = load_df(c_frontend, c_repository)

button_text = "Enable editing" if not get_state(State.EDITING_ENABLED) else "Disable editing"
button_type = "primary" if not get_state(State.EDITING_ENABLED) else "secondary"
control_btns_cols[0].button(button_text, type=button_type, on_click=lambda: toggle_state(State.EDITING_ENABLED))

# TODO below code is with confirmation
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


# ---------------- display changes ----------------


if is_data_edited():
    deleted_rows = get_state(State.DATA_EDITOR)["deleted_rows"]
    if deleted_rows:
        deleted_idxs = df.iloc[deleted_rows].index
        deleted_rows_df = df.loc[deleted_idxs]
        with st.expander("Deleted rows:", expanded=True):
            st.dataframe(
                deleted_rows_df,
                use_container_width=True,
                column_order=c_frontend.column_order,
                column_config=c_frontend.column_config,
            )

    clear_outdated_data_editor_edits(df)
    edited_rows = get_state(State.DATA_EDITOR)["edited_rows"]
    if edited_rows:
        edited_idxs = df.iloc[map(int, edited_rows.keys())].index
        edited_rows_df = df.loc[edited_idxs]
        with st.expander("Edited rows (Showing original values):", expanded=True):
            st.dataframe(
                edited_rows_df,
                use_container_width=True,
                column_order=c_frontend.column_order,
                column_config=c_frontend.column_config,
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
    column_order=c_frontend.column_order,
    column_config=c_frontend.column_config,
    disabled=not get_state(State.EDITING_ENABLED),
    num_rows="dynamic" if get_state(State.EDITING_ENABLED) else "fixed",
    key=State.DATA_EDITOR
)


def debug_state():
    col1, col2 = st.columns((1, 3))
    col1.write(get_state(State.DATA_EDITOR))
    col2.write(st.session_state)


debug_state()
