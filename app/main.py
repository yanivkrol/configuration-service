import warnings
from collections import defaultdict

import pandas as pd
from pandas import DataFrame

from configuration_frontend.base_configuration_frontend import BaseConfigurationFrontend
from configurations import get_all_configurations

warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
from st_oauth import st_oauth

import process_changes

import configuration_frontend
import repository.configuration as configuration_repository
from repository.configuration.configuration_repository import ConfigurationRepository
from components.filter_dataframe import filter_df
from state_management import *


def is_data_edited():
    data_editor = get_state(State.DATA_EDITOR)
    if data_editor and bool(data_editor["edited_rows"] or data_editor["deleted_rows"]):
        return True
    return False


def load_df(c_frontend: BaseConfigurationFrontend, c_repository: ConfigurationRepository):
    df = c_repository.get_as_df(limit=QUERY_SIZE_LIMIT)
    df = filter_df(df, c_frontend)
    return df


def is_disabled_btn_enable_editing():
    if get_state(State.CONFIRMING_SAVE):
        return True
    return False


def clicked_btn_enable_editing():
    toggle_state(State.EDITING)


def is_disabled_btn_add_new():
    if get_state(State.CONFIRMING_SAVE):
        return True
    return False


def clicked_btn_add_new():
    set_state(State.ADDING_NEW, True)


def is_disabled_btn_save():
    if not is_data_edited() and not get_state(State.NEW_DATA):
        return True
    if get_state(State.CONFIRMING_SAVE):
        return True
    if get_state(State.CONFIRMED_SAVE):
        return True
    return False


def clicked_btn_save():
    set_state(State.CONFIRMING_SAVE, True)
    cancel_add_new()


def cancel_add_new():
    set_state(State.ADDING_NEW, False)
    clear_add_new_states()


def clicked_btn_cancel_add_new():
    cancel_add_new()


def clicked_btn_cancel_save():
    set_state(State.CONFIRMING_SAVE, False)


def clicked_btn_continue_save(df):
    set_state(State.CONFIRMING_SAVE, False)
    with st.spinner("Saving..."):
        data_editor = get_state(State.DATA_EDITOR)
        new_data = get_state(State.NEW_DATA)
        process_changes.apply_changes(c_repository, df, data_editor["deleted_rows"], data_editor["edited_rows"], new_data)
        st.cache_data.clear()  # TODO maybe we will have api to clear specific keys in the future
        reset_main_section_state()
        st.markdown("""<div style="margin-top: 25px;"></div>""", unsafe_allow_html=True)
        st.success("Saved successfully!", icon="🚀")


def is_disabled_btn_add_add_new():
    if all(v for k, v in st.session_state.items() if k.startswith("add_new_")):
        return False
    return True


def clicked_btn_add_add_new():
    set_state(State.ADDING_NEW, False)

    new_data = {}
    for k in st.session_state:
        if k.startswith("add_new_"):
            new_data[k.replace("add_new_", "")] = st.session_state.pop(k)

    set_state(State.NEW_DATA, [*get_state(State.NEW_DATA), new_data])


companies = [
    {"shortened": "ni", "full": "Natural Intelligence", "domain": "naturalint.com"},
    {"shortened": "bi", "full": "Better Impression", "domain": "bimpression.com"},
    {"shortened": "cappsool", "full": "Cappsool", "domain": "cappsool.com"},
]
QUERY_SIZE_LIMIT = 10

st.set_page_config(layout="wide")

user_email = st_oauth(label='Login with Okta') if st.secrets['use_login'] else "john.doe@naturalint.com"

# remove margin
st.markdown("""
  <style>
    .block-container {
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)

init_default_states()
# if not get_state(State.EDITING_ENABLED):
#     reset_main_section_state()

# ------------------ sidebar ------------------


with st.sidebar.container():
    st.title("Configuration Service")
    name, domain = user_email.split('@')
    st.write(f"Hello {name.split('.')[0].title()}!")

    st.divider()

    st.selectbox(
        label="Company:",
        options=companies,
        format_func=lambda c: c['full'],
        index=[c['domain'] for c in companies].index(domain),
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


col1, col2, margin, col3 = st.columns((1, 1, 5, 1))

button_text = "Enable editing" if not get_state(State.EDITING) else "Disable editing"
button_type = "primary" if not get_state(State.EDITING) else "secondary"
col1.button(button_text,
            type=button_type,
            disabled=is_disabled_btn_enable_editing(),
            on_click=clicked_btn_enable_editing,
            use_container_width=True)

col2.button("Add new",
            type="primary",
            disabled=is_disabled_btn_add_new(),
            on_click=clicked_btn_add_new,
            use_container_width=True)

col3.button("Save",
            type="primary",
            disabled=is_disabled_btn_save(),
            on_click=clicked_btn_save,
            use_container_width=True)

if get_state(State.CONFIRMING_SAVE):
    # TODO maybe Modal (not officially released yet https://experimental-modals.streamlit.app/)
    # TODO possible to use https://pypi.org/project/streamlit-modal/ in the meanwhile
    st.write("You are about to apply the changes to the database. Please review them below before continuing.")
    col1, col2, margin = st.columns((1, 1, 6))
    col1.button("Cancel", type="secondary", on_click=clicked_btn_cancel_save, use_container_width=True)
    col2.button("Continue", type="primary", on_click=lambda: clicked_btn_continue_save(df), use_container_width=True)

# if get_state(State.SAVE_CONFIRMED):
#     set_state(State.SAVE_CONFIRMED, False)
#     with st.spinner("Saving..."):
#         data_editor = get_state(State.DATA_EDITOR)
#         process_changes.apply_changes(c_repository, df, data_editor["deleted_rows"], data_editor["edited_rows"])
#         st.cache_data.clear()  # TODO maybe we will have api to clear specific keys in the future
#         reset_main_section_state()
#         st.success("Saved successfully!", icon="🚀")
#         df = load_df(c_frontend, c_repository)


# ---------------- display changes ----------------

def create_new_configurations_df(new_data):
    new_data_flattened = defaultdict(list)
    for row in new_data:
        row_flattened = {k: v for model in row.values() for k, v in model.as_dict().items()}  # TODO values which are not models
        row_flattened['active'] = 1
        for k, v in row_flattened.items():
            new_data_flattened[k].append(v)
    return pd.DataFrame(new_data_flattened)


def display_changes():
    new_data = get_state(State.NEW_DATA)
    deleted_rows, edited_rows, added_rows = None, None, None
    if get_state(State.DATA_EDITOR):
        deleted_rows = get_state(State.DATA_EDITOR)["deleted_rows"]
        clear_outdated_data_editor_edits(df)
        edited_rows = get_state(State.DATA_EDITOR)["edited_rows"]
        added_rows = get_state(State.DATA_EDITOR)["added_rows"]

    if any([new_data, deleted_rows, edited_rows]):
        with st.expander("Changes: (Click 'Save' to apply)", expanded=False):

            if new_data:
                new_configs_df = create_new_configurations_df(new_data)
                st.write("New configurations:")
                st.dataframe(
                    new_configs_df,
                    hide_index=True,
                    use_container_width=True,
                    column_order=c_frontend.column_order,
                    column_config=c_frontend.column_config,
                )

            if deleted_rows:
                deleted_idxs = df.iloc[deleted_rows].index
                deleted_rows_df = df.loc[deleted_idxs]
                st.write("Deleted configurations:")
                st.dataframe(
                    deleted_rows_df,
                    use_container_width=True,
                    column_order=c_frontend.column_order,
                    column_config=c_frontend.column_config,
                )

            if edited_rows:
                edited_idxs = df.iloc[map(int, edited_rows.keys())].index
                edited_rows_df = df.loc[edited_idxs]
                st.write("Edited configurations (Showing original values):")
                st.dataframe(
                    edited_rows_df,
                    use_container_width=True,
                    column_order=c_frontend.column_order,
                    column_config=c_frontend.column_config,
                )

    # Don't allow adding rows directly to the dataframe
    if added_rows:
        st.warning("Adding rows directly to the table is not supported. " +
                   "Any changes will not be saved.")


display_changes()

# ------------------ data editor ------------------

curr_editor_has_modifications = is_data_edited()


def display_data_editor():
    # https://docs.streamlit.io/library/advanced-features/dataframes
    st.data_editor(
        df,
        use_container_width=True,
        column_order=c_frontend.column_order,
        column_config=c_frontend.column_config,
        disabled=not get_state(State.EDITING),
        num_rows="dynamic" if get_state(State.EDITING) else "fixed",
        key=State.DATA_EDITOR
    )


display_data_editor()

if is_data_edited() != curr_editor_has_modifications:
    # When we disable editing, the changes section shows the changes
    # but calling st.data_editor clears the data_editor (because of the 'disabled' keyword),
    # so we rerun the script to remove the changes display
    st.rerun()


# ------------------ add new ------------------


def display_add_new_section():
    st.divider()
    st.write("New configuration:")
    c_frontend.render_new_section()
    margin, col1, col2 = st.columns((10, 1, 1))
    col1.button("Cancel", on_click=clicked_btn_cancel_add_new, use_container_width=True)
    col2.button("Add", type="primary", on_click=clicked_btn_add_add_new, disabled=is_disabled_btn_add_add_new(), use_container_width=True)


if get_state(State.ADDING_NEW):
    display_add_new_section()


# ------------------ debug ------------------


def debug_state():
    with st.expander("debug", expanded=True):
        col1, col2, col3 = st.columns((1, 1, 1))
        col1.write({k: v for k, v in st.session_state.items()
                    if k not in ["_StateKey.DATA_EDITOR", "_StateKey.NEW_DATA"]})
        col2.write(get_state(State.DATA_EDITOR))
        col3.write(get_state(State.NEW_DATA))


debug_state()
