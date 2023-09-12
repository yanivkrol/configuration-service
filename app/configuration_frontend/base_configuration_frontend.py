from abc import ABC
from typing import Optional, Callable

from streamlit.elements.lib.column_types import ColumnConfig


class BaseConfigurationFrontend(ABC):  # TODO if there are only variables and no behavior, make it a class instead of an ABC and no subclasses

    def __init__(self,
                 name: str,
                 column_order: Optional[list[str]] = None,
                 column_config: Optional[dict[str, ColumnConfig]] = None,
                 filter_column_choices: Optional[dict[str, list[str]]] = None,
                 create_fields_config: Optional[dict[str, Callable]] = None):
        self.name = name
        self.column_order = column_order or []
        self.column_config = column_config or {}
        self.filter_column_choices = filter_column_choices or {}
        self.create_fields_config = create_fields_config or {}
