from typing import List

import pandas as pd

from app.frontend.confiugration import Selection
from db_config import db_session
from .configuration import BaseConfigurationMiddleware
from repository.configuration import ConfigurationRepository


def apply_changes(repo: ConfigurationRepository,
                  middleware: BaseConfigurationMiddleware,
                  filtered_df: pd.DataFrame,
                  deleted_rows: List[int],
                  edited_rows: dict[str, dict],
                  new_data: list[Selection]):
    try:
        _apply_additions(repo, middleware, new_data)
        _apply_deletions(repo, filtered_df, deleted_rows)
        _apply_edits(repo, filtered_df, edited_rows)
        db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        raise


def _apply_deletions(repo: ConfigurationRepository, filtered_df: pd.DataFrame, deleted_rows: List[int]):
    deleted_idxs = filtered_df.iloc[deleted_rows].index
    if len(deleted_idxs) > 0:
        for id in deleted_idxs:
            repo.delete(id)


def _apply_edits(repo: ConfigurationRepository, filtered_df: pd.DataFrame, edited_rows: dict[str, dict]):
    for row_num, row_changes in edited_rows.items():
        id = filtered_df.iloc[int(row_num)].name
        repo.update(id, row_changes)


def _apply_additions(repo: ConfigurationRepository, middleware: BaseConfigurationMiddleware, new_data: list[Selection]):
    for selection in new_data:
        repo.add(middleware.to_database_object(selection))
