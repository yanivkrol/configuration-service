from typing import List

import pandas as pd
import streamlit as st

from app.frontend.confiugration import Selection
from db_config import SessionMaker
from .configuration import BaseConfigurationMiddleware
from .database_interface import DatabaseInterface


class ChangesApplier:
    def __init__(self,
                 c_middleware: BaseConfigurationMiddleware,
                 filtered_df: pd.DataFrame,
                 deleted_rows: List[int],
                 edited_rows: dict[str, dict],
                 new_data: list[Selection]):
        self.c_middleware = c_middleware
        self.filtered_df = filtered_df
        self.deleted_rows = deleted_rows
        self.edited_rows = edited_rows
        self.new_data = new_data
        self.db_session = SessionMaker()
        self.db_interface = DatabaseInterface(self.c_middleware.get_model_type(), self.db_session)

    def apply_changes(self):
        try:
            self._apply_additions()
            self._apply_deletions()
            self._apply_edits()
            self.db_session.commit()
        except Exception as e:
            print(e)
            self.db_session.rollback()
            raise
        self._clear_configurations_cache()

    def _apply_additions(self):
        for selection in self.new_data:
            self.db_interface.add(self.c_middleware.to_database_object(selection))

    def _apply_deletions(self):
        deleted_idxs = self.filtered_df.iloc[self.deleted_rows].index
        if len(deleted_idxs) > 0:
            for id in deleted_idxs:
                self.db_interface.delete(id)

    def _apply_edits(self):
        for row_num, row_changes in self.edited_rows.items():
            id = self.filtered_df.iloc[int(row_num)].name
            self.db_interface.update(id, row_changes)

    def _clear_configurations_cache(self):
        st.cache_data.clear()
