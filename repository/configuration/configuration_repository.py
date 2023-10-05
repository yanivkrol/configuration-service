from abc import abstractmethod
from typing import TypeVar, Type, Optional, Generic

import pandas as pd
import streamlit as st
from sqlalchemy import desc
from sqlalchemy.orm import Session, Query

from app.configuration_frontend import Selection
from model.serializable_model import SerializableModel
from repository.base_repository import BaseRepository, hash_query

ConfigurationModelT = TypeVar('ConfigurationModelT', bound=SerializableModel)
SelectionT = TypeVar('SelectionT', bound=Selection)


class ConfigurationRepository(BaseRepository[ConfigurationModelT], Generic[ConfigurationModelT, SelectionT]):
    def __init__(self, model: Type[ConfigurationModelT], session: Session):
        super().__init__(model, session)

    def get_as_df(self, limit: Optional[int] = None) -> pd.DataFrame:  # TODO remove limit in all places?
        query = self._get_as_df_query().order_by(desc(self.model.id)).limit(limit)  # type: ignore
        return self._cached_pd_read_sql(query)

    @staticmethod
    @st.cache_data(ttl=300, show_spinner="Loading data...", hash_funcs={Query: hash_query})
    def _cached_pd_read_sql(query: Query) -> pd.DataFrame:
        return pd.read_sql(query.statement, query.session.bind, index_col="id")

    @abstractmethod
    def _get_as_df_query(self) -> Query:
        ...

    @abstractmethod
    def add_from_selections(self, selections: list[SelectionT]):  # TODO better name and API
        ...
