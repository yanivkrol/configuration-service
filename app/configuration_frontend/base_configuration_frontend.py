from abc import ABC, abstractmethod

import streamlit as st


class BaseConfigurationFrontend(ABC):

    def __init__(self,
                 name: str,
                 display_name_mapping: dict[str, str]):
        self.name = name

        self.column_config = {'id': st.column_config.NumberColumn(
            label="ID",
        )}
        self.column_config.update({
            column: st.column_config.TextColumn(
                    label=display_name,
                    disabled=True,  # No editing values
                )
            for column, display_name in display_name_mapping.items()
        })
        self.column_config['active'] = st.column_config.CheckboxColumn(
            label="Active",
            width="small",
        )

        self.column_order = list(self.column_config.keys())
        self.column_order.remove("id")

        self.display_name_mapping = {k: cfg['label'] for k, cfg in self.column_config.items()}
        self.display_name_mapping.pop("id")

    @abstractmethod
    def render_new_section(self):
        ...
