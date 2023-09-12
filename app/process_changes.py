from typing import List

import pandas as pd

from repository.configuration_repository import ConfigurationRepository


def apply_changes(repo: ConfigurationRepository, df: pd.DataFrame, deleted_rows: List[int], edited_rows: dict[str, dict]):
    deleted_idxs = df.iloc[deleted_rows].index
    if len(deleted_idxs) > 0:
        for id in deleted_idxs:
            repo.delete(id)

    for row_num, row_changes in edited_rows.items():
        # for column_name, new_value in row_changes.items():
        id = df.iloc[int(row_num)].name
        repo.update(id, row_changes)
        #
        # record = repo.clazz(**df.iloc[int(row_num)].to_dict())
        # repo.update_record(record['id'], record)



    # repo.update_record(df, edited_rows)  # TODO edited