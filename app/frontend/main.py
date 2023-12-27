import streamlit as st
from sqlalchemy.exc import IntegrityError
from st_oauth import st_oauth

st.set_page_config(layout="wide")

from configurations import get_all_configurations
from app.middleware import middleware
import app.frontend.confiugration as confiugration_frontend
import repository.configuration as configuration_repository
import app.middleware.configuration as configuration_middleware
from state_management import *


def is_data_edited():
    data_editor = get_state(State.DATA_EDITOR)
    if data_editor and bool(data_editor["edited_rows"] or data_editor["deleted_rows"]):
        return True
    return False


def is_disabled_btn_edit():
    if get_state(State.CONFIRMING_SAVE):
        return True
    return False


def clicked_btn_edit():
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


def clicked_btn_cancel_add_new():
    cancel_add_new()


def clicked_btn_cancel_save():
    set_state(State.CONFIRMING_SAVE, False)


def clicked_btn_continue_save(df):
    set_state(State.CONFIRMING_SAVE, False)
    with st.spinner("Saving..."):
        data_editor = get_state(State.DATA_EDITOR)
        new_data = get_state(State.NEW_DATA)
        try:
            middleware.apply_changes(c_repository, c_middleware, df, data_editor["deleted_rows"],
                                     data_editor["edited_rows"], new_data)
        except IntegrityError as e:
            if "Duplicate entry" in str(e.orig):
                handle_save_error(e, "Configuration already exists.")
            else:
                handle_save_error(e, str(e.orig))
            return
        except Exception as e:
            handle_save_error(e)
            return
        handle_save_success()


def handle_save_error(e: Exception, err_msg: str = None):
    st.markdown("""<div style="margin-top: 25px;"></div>""", unsafe_allow_html=True)
    st.error("Failed to save changes. " + (err_msg or str(e)))


def handle_save_success():
    reset_main_section_state()
    st.markdown("""<div style="margin-top: 25px;"></div>""", unsafe_allow_html=True)
    st.success("Saved successfully!", icon="🚀")
    st.warning("Changes may take some time to take effect.", icon="⚠")


def is_disabled_btn_add_add_new():
    if get_state(State.NEW_CONFIGURATION):
        return False
    return True


def clicked_btn_add_add_new():
    set_state(State.ADDING_NEW, False)
    get_state(State.NEW_DATA).append(get_state(State.NEW_CONFIGURATION))


companies = [
    {
        "shortened": "ni",
        "full": "Natural Intelligence",
        "domain": "naturalint.com"
    },
    {
        "shortened": "bi",
        "full": "Better Impression",
        "domain": "bimpression.com"
    },
    {
        "shortened": "cappsool",
        "full": "Cappsool",
        "domain": "cappsool.com"
    },
]


user_email = st_oauth(label='Login with Okta') if st.secrets['use_login'] else "john.doe@naturalint.com"  # TODO env var

init_default_states()


# remove margin
st.markdown("""
  <style>
    .block-container {
      margin-top: -75px;
    }
  </style>
""", unsafe_allow_html=True)

# ------------------ sidebar ------------------


with st.sidebar.container():
    st.title("Configuration Service")
    name, domain = user_email.split('@')
    st.write(f"Hello {name.split('.')[0].title()}! 👋🏼")

    st.divider()

    st.selectbox(
        label="Company:",
        options=companies,
        format_func=lambda c: c['full'],
        index=[c['domain'] for c in companies].index(domain),
        on_change=reset_main_section_state,
        key=State.COMPANY
    )

    st.selectbox(
        label="Configuration:",
        options=get_all_configurations(),
        format_func=lambda c: confiugration_frontend.get_frontend(c).label,
        on_change=reset_main_section_state,
        key=State.CONFIGURATION
    )

    st.divider()

c_frontend = confiugration_frontend.get_frontend(get_state(State.CONFIGURATION))
c_repository = configuration_repository.get_repository(get_state(State.CONFIGURATION))
c_middleware = configuration_middleware.get_middleware(get_state(State.CONFIGURATION))

full_df = c_repository.get_as_df()
with st.sidebar.container():
    editing = get_state(State.EDITING)
    "Filters:"
    filtered_df = c_frontend.render_filters(full_df, disabled=editing)
    set_state(State.FILTERED_DF, filtered_df)
    if editing:
        "﹡Further filtering is disabled when editing."


# ------------------ main section ------------------


st.title(c_frontend.label)


# ------------------ control buttons ------------------


col1, col2, margin, col3 = st.columns((1, 1, 5, 1))

if not get_state(State.EDITING):
    button_text = "Enable editing"
elif is_data_edited():
    button_text = "Undo changes"
else:
    button_text = "Disable editing"
button_type = "primary" if not get_state(State.EDITING) else "secondary"
col1.button(button_text,
            type=button_type,
            disabled=is_disabled_btn_edit(),
            on_click=clicked_btn_edit,
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
    col2.button("Continue", type="primary", on_click=lambda: clicked_btn_continue_save(filtered_df), use_container_width=True)


# ---------------- display changes ----------------


def display_changes():
    new_data = get_state(State.NEW_DATA)
    deleted_rows, edited_rows, added_rows = None, None, None
    if get_state(State.DATA_EDITOR):
        deleted_rows = get_state(State.DATA_EDITOR)["deleted_rows"]
        clear_outdated_data_editor_edits(filtered_df)
        edited_rows = get_state(State.DATA_EDITOR)["edited_rows"]
        added_rows = get_state(State.DATA_EDITOR)["added_rows"]

    if any([new_data, deleted_rows, edited_rows]):
        with st.expander("Changes: (Click 'Save' to apply)", expanded=False):
            st.markdown("""
              <style>
                details {
                    background-color: rgba(255, 227, 18, 0.1);
                }
              </style>
            """, unsafe_allow_html=True)

            if new_data:
                new_configs_df = c_frontend.create_df_from_selections(new_data)
                st.write("New configurations:")
                st.dataframe(
                    c_frontend.get_df_for_display(new_configs_df),
                    hide_index=True,
                    use_container_width=True,
                    column_order=c_frontend.column_order,
                    column_config=c_frontend.column_config,
                )

            if deleted_rows:
                deleted_idxs = filtered_df.iloc[deleted_rows].index
                deleted_rows_df = filtered_df.loc[deleted_idxs]
                st.write("Deleted configurations:")
                st.dataframe(
                    c_frontend.get_df_for_display(deleted_rows_df),
                    use_container_width=True,
                    column_order=c_frontend.column_order,
                    column_config=c_frontend.column_config,
                )

            if edited_rows:
                edited_idxs = filtered_df.iloc[map(int, edited_rows.keys())].index
                edited_rows_df = filtered_df.loc[edited_idxs]
                st.write("Edited configurations (Showing original values):")
                st.dataframe(
                    c_frontend.get_df_for_display(edited_rows_df),
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
        c_frontend.get_df_for_display(filtered_df),
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
    selection = c_frontend.render_new_section()
    set_state(State.NEW_CONFIGURATION, selection)
    margin, col1, col2 = st.columns((10, 1, 1))
    col1.button("Cancel", on_click=clicked_btn_cancel_add_new, use_container_width=True)
    col2.button("Add", type="primary", on_click=clicked_btn_add_add_new, disabled=is_disabled_btn_add_add_new(),
                use_container_width=True)


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


if st.secrets['debug']:
    debug_state()
