from typing import List

import pandas as pd

from app.configuration_frontend import Selection
from db_config import db_session
from repository.configuration.configuration_repository import ConfigurationRepository


def apply_changes(repo: ConfigurationRepository,
                  filtered_df: pd.DataFrame,
                  deleted_rows: List[int],
                  edited_rows: dict[str, dict],
                  new_data: list[Selection]):
    deleted_idxs = filtered_df.iloc[deleted_rows].index
    if len(deleted_idxs) > 0:
        for id in deleted_idxs:
            repo.delete(id)

    for row_num, row_changes in edited_rows.items():
        # for column_name, new_value in row_changes.items():
        id = filtered_df.iloc[int(row_num)].name
        repo.update(id, row_changes)
        #
        # record = repo.clazz(**df.iloc[int(row_num)].to_dict())
        # repo.update_record(record['id'], record)

    repo.add_from_selections(new_data)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        raise