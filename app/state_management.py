from enum import Enum, auto
from typing import Optional, Any

import pandas as pd
import streamlit as st


class _StateKey(Enum):
    COMPANY = auto()
    CONFIGURATION = auto()
    EDITING = auto()
    DATA_EDITOR = auto()
    ADDING_NEW = auto()
    NEW_CONFIGURATION = auto()
    NEW_DATA = auto()
    CONFIRMING_SAVE = auto()
    CONFIRMED_SAVE = auto()


State = _StateKey


def init_state(key: _StateKey, value: Any) -> None:
    if key not in st.session_state:
        st.session_state[key] = value


def set_state(key: _StateKey, value: Any) -> None:
    st.session_state[key] = value


def get_state(key: _StateKey) -> Optional[Any]:
    return st.session_state.get(key, None)


def del_state(key: _StateKey) -> None:
    try:
        del st.session_state[key]
    except KeyError:
        pass


def toggle_state(key: _StateKey) -> None:
    assert isinstance(st.session_state[key], bool)
    st.session_state[key] = not st.session_state[key]


def reset_main_section_state():
    set_state(State.EDITING, False)
    del_state(State.DATA_EDITOR)
    set_state(State.ADDING_NEW, False)
    set_state(State.NEW_CONFIGURATION, None)
    set_state(State.NEW_DATA, [])
    set_state(State.CONFIRMING_SAVE, False)
    set_state(State.CONFIRMED_SAVE, False)


def init_default_states():
    init_state(State.EDITING, False)
    init_state(State.ADDING_NEW, False)
    set_state(State.NEW_CONFIGURATION, None)
    init_state(State.NEW_DATA, [])
    init_state(State.CONFIRMING_SAVE, False)
    init_state(State.CONFIRMED_SAVE, False)


def clear_outdated_data_editor_edits(df: pd.DataFrame) -> None:
    """
    If an edit is reverted, the editor doesn't automatically remove it from the state,
    so we need to do it manually, by comparing the changes to the original values.
    """
    edited_rows_items = list(get_state(State.DATA_EDITOR)["edited_rows"].items())
    for row_num, row_changes in edited_rows_items:
        row_changes_items = list(row_changes.items())
        for column_name, new_value in row_changes_items:
            if new_value == df.iloc[int(row_num)][column_name]:
                row_changes.pop(column_name)
        if len(row_changes) == 0:
            get_state(State.DATA_EDITOR)["edited_rows"].pop(row_num)
