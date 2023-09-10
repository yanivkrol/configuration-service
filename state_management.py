from enum import Enum, auto
from typing import Optional, Any

import streamlit as st


class _StateKey(Enum):
    COMPANY = auto()
    CONFIGURATION = auto()
    EDITING_ENABLED = auto()
    SAVE_CLICKED = auto()
    SAVE_CONFIRMED = auto()
    DF = auto()
    DATA_EDITOR = auto()


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
