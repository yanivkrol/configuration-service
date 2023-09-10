from abc import ABC
from typing import Optional, List

from streamlit.elements.lib.column_types import ColumnConfig


class Configuration(ABC):   # TODO if there are only variables and no behavior, make it a class instead of an ABC

    def __init__(self, name: str, id_column: str, tables: List[dict[str, str]],  # TODO docs
                 column_order: Optional[list[str]] = None,
                 column_config: Optional[dict[str, ColumnConfig]] = None,
                 filter_column_choices: Optional[dict[str, list[str]]] = None):
        self.name = name
        self.id_column = id_column
        self.tables = tables  # TODO we will have multiple tables per config? what to do about it?
        self.column_order = column_order or []
        self.column_config = column_config or {}
        self.filter_column_choices = filter_column_choices or {}
